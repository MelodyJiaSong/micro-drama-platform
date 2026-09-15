// Real .exe front for fake_dreamina.py (tests only). Compiled at test time with the .NET Framework csc.exe,
// so the client under test launches a genuine .exe with no launcher prefix — the same path production uses.
using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading.Tasks;

internal static class FakeDreaminaLauncher
{
    private static int Main(string[] args)
    {
        string python = Environment.GetEnvironmentVariable("FAKE_DREAMINA_PYTHON");
        string script = Environment.GetEnvironmentVariable("FAKE_DREAMINA_SCRIPT");
        var commandLine = new StringBuilder();
        AppendQuoted(commandLine, script);
        foreach (string arg in args)
        {
            commandLine.Append(' ');
            AppendQuoted(commandLine, arg);
        }
        var start = new ProcessStartInfo(python, commandLine.ToString())
        {
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
        };
        using (Process child = Process.Start(start))
        {
            Task stdout = child.StandardOutput.BaseStream.CopyToAsync(Console.OpenStandardOutput());
            Task stderr = child.StandardError.BaseStream.CopyToAsync(Console.OpenStandardError());
            child.WaitForExit();
            Task.WaitAll(stdout, stderr);
            return child.ExitCode;
        }
    }

    // Standard Windows argv quoting (inverse of CommandLineToArgvW): double backslashes that precede a quote.
    private static void AppendQuoted(StringBuilder builder, string arg)
    {
        if (arg.Length > 0 && arg.IndexOfAny(new[] { ' ', '\t', '\n', '\v', '"' }) < 0)
        {
            builder.Append(arg);
            return;
        }
        builder.Append('"');
        int backslashes = 0;
        foreach (char c in arg)
        {
            if (c == '\\')
            {
                backslashes++;
                continue;
            }
            if (c == '"')
            {
                builder.Append('\\', backslashes * 2 + 1);
                builder.Append('"');
            }
            else
            {
                builder.Append('\\', backslashes);
                builder.Append(c);
            }
            backslashes = 0;
        }
        builder.Append('\\', backslashes * 2);
        builder.Append('"');
    }
}
