import sys
from pathlib import Path
from typing import Annotated, Any

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from pydantic import Field
from projects.suno_browser_service.libs.application.commands.agent__command import AgentCommand
from projects.suno_browser_service.libs.application.queries.agent__query import AgentQuery
from projects.suno_browser_service.libs.common.generation import GenerationRequest

server = FastMCP("suno-browser", instructions="所有新音频生成的默认入口：环境音/音效用 Sounds，配乐用 Advanced 纯音乐，歌曲用 Advanced 歌词或 Simple。先 suno_capabilities 再 suno_plan；能力不足或验证码暂停时不自动换引擎。准确 TTS、声线克隆和分离人声尚未支持；混音/剪辑沿用后期工具。Create 使用用户付费 Suno 账号；固定幂等键并查询同一 job，needs_login/needs_attention/uncertain 时停止。上传先存本机，正式任务才发送 Suno。未知提交不能换键重提、不绕过验证码。网页选项生成前读回，真实联调未完成。工具参数和结构化结果见各工具描述，HTTP 说明在本机 /docs。")
read_only = ToolAnnotations(readOnlyHint=True, destructiveHint=False, idempotentHint=True, openWorldHint=False)
local_write = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=False)
paid_write = ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True, openWorldHint=True)


@server.tool(annotations=read_only)
def suno_capabilities() -> dict[str, Any]:
    """第一步：读取 request_schema、modes、uploads、automation_paused 和 evidence。只读本机，不访问 Suno、不收费。implemented 不等于 live_verified；暂停时不要新建收费任务。"""
    return AgentQuery().capabilities()


@server.tool(annotations=read_only)
def suno_plan(request: Annotated[GenerationRequest, Field(description="待生成的完整请求，与随后 suno_create 的 request 保持一致。")]) -> dict[str, Any]:
    """提交前预检 schema 与本机参考文件，返回 request、references、warnings 和暂停状态。不建任务、不操作浏览器、不收费；不保证页面或素材组合可用，Create 时仍校验。"""
    return AgentQuery().plan(request)


@server.tool(annotations=local_write)
def suno_upload_reference(path: Annotated[str, Field(description="运行 MCP 的电脑上的媒体文件路径，建议绝对路径；不是网络 URL。")],
                          rights_confirmed: Annotated[bool, Field(description="明确有权使用该素材才设 true；不确认时遇 Suno 权利弹窗会暂停。")]=False) -> dict[str, Any]:
    """将音频/图片/视频保存本机，最多 64 MiB；返回 id、kind、bytes、sha256、rights_confirmed。把返回 id 放入 request.references[].asset_id。此步不上传 Suno、不收费。"""
    return AgentCommand().upload(path, rights_confirmed)


@server.tool(annotations=paid_write)
def suno_create(request: Annotated[GenerationRequest, Field(description="已预检的生成请求；执行时会把参考上传 Suno，并可能消耗积分和下载额度。")],
                idempotency_key: Annotated[str, Field(description="同一次生成固定使用的 1–128 位 ASCII 字母、数字或 _.:-；同键同参数返回原任务，改参数返回冲突。", min_length=1, max_length=128, pattern=r"^[A-Za-z0-9_.:-]+$")]) -> dict[str, Any]:
    """排队生成并经官方下载，返回 Job（id/status/request/next_action/song_urls/files/error/applied_options），不等于已完成。先 capabilities、plan；再对返回 id 调 wait/get。超时沿用原键；未知提交不能换键重提。"""
    return AgentCommand().create(request, idempotency_key)


@server.tool(annotations=read_only)
def suno_get_job(job_id: Annotated[str, Field(description="create/list 返回的 32 位十六进制任务 id。")]) -> dict[str, Any]:
    """只读本机 Job。status=completed 才进入成品交付；applied_options 是网页已读回值，files 为已登记文件，error 和 next_action 指导恢复。不会查询 Suno 或再次生成。"""
    return AgentQuery().get(job_id)


@server.tool(annotations=read_only)
def suno_list_jobs() -> list[dict[str, Any]]:
    """返回最近 100 个本机 Job（包含暂停和结果未知任务），用于找回已有 id，避免重复生成。不查询付费服务；MCP structuredContent.result 为列表。"""
    return AgentQuery().list()


@server.tool(annotations=read_only)
def suno_wait_job(job_id: Annotated[str, Field(description="要等待的已有任务 id，不创建新任务。")],
                  seconds: Annotated[int, Field(description="最多等待秒数，0 为立即查询；超时继续等待同一 job。", ge=0, le=45)] = 45) -> dict[str, Any]:
    """轮询本机 API，返回 {job,timed_out}，队列暂停时可附 automation_paused/next_action。completed、needs_login、needs_attention、uncertain 会提前返回；timed_out 不是生成失败。"""
    return AgentQuery().wait(job_id, seconds)


@server.tool(annotations=local_write)
def suno_cancel_job(job_id: Annotated[str, Field(description="尚未提交（从未点 Create）的 queued/needs_login/needs_attention 任务 id。")]) -> dict[str, Any]:
    """取消尚未提交的任务，返回 Job（status=cancelled）；不访问 Suno。已提交任务拒绝取消。"""
    return AgentCommand().cancel(job_id)


@server.tool(annotations=paid_write)
def suno_resume_job(job_id: Annotated[str, Field(description="needs_login/needs_attention/uncertain 的已有任务 id；执行中或已完成任务不可恢复。")],
                    song_urls: Annotated[list[str], Field(description="最多两条已确认属于该任务的 https://suno.com/song/<UUID>。已提交且结果未知必须提供（或改用 recollect）；已存歌曲或确定尚未提交可传 []。", max_length=2)],
                    recollect: Annotated[bool, Field(description="已提交但结果未知或认领有误：只在库里按标题 / Sounds prompt 重新认领，不重新生成；不能与 song_urls 同用。")] = False) -> dict[str, Any]:
    """修复原因后将原任务重新排队，返回 Job；不清除全局验证码暂停。带已确认歌曲只补下载；确定尚未提交的任务恢复后会首次 Create 并可能收费。未知提交没有歌曲时拒绝恢复。"""
    return AgentCommand().resume(job_id, song_urls, recollect)


@server.tool(annotations=local_write)
def suno_download(job_id: Annotated[str, Field(description="已有任务 id；通常等 completed 后下载，部分完成时只返回已登记文件。")],
                  output_directory: Annotated[str, Field(description="运行 MCP 的电脑上的输出目录，建议绝对路径；缺目录会创建。")]) -> dict[str, Any]:
    """从本机 API 复制已登记音频并校验大小/SHA256；不再次调用 Suno。返回 {job_id,status,files,next_action}，files 每项含 path。同名不同内容保留并报错；空 files 不代表成功生成。"""
    return AgentCommand().download(job_id, output_directory)


if __name__ == "__main__":
    server.run(transport="stdio")
