from dataclasses import dataclass

from libs.common.enums import RefKind
from libs.domain.errors.precheck__error import InvalidRequestError


@dataclass(frozen=True)
class ReferenceItem:
    name: str
    label: str
    kind: RefKind
    resolved_path: str | None = None
    entity_name: str | None = None
    sha256: str | None = None

    def __post_init__(self) -> None:
        if not self.name:
            raise InvalidRequestError("参考项 name 不能为空")
        if self.kind is RefKind.ENTITY:
            if not self.entity_name:
                raise InvalidRequestError(f"主体参考项 {self.name} 缺少 entity_name")
            if self.resolved_path is not None or self.sha256 is not None:
                raise InvalidRequestError(f"主体参考项 {self.name} 不能带文件路径或 sha256")
        elif self.entity_name is not None:
            raise InvalidRequestError(f"文件参考项 {self.name} 不能带 entity_name")

    @property
    def is_entity(self) -> bool:
        return self.kind is RefKind.ENTITY

    def canonical(self) -> dict[str, object]:
        if self.is_entity:
            return {"kind": self.kind.value, "name": self.name, "entity": self.entity_name}
        return {"kind": self.kind.value, "name": self.name, "sha256": self.sha256}
