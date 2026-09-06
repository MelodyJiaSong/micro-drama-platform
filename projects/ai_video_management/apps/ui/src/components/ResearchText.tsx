/** Renders the research dataset's prose, which uses `**bold**` for the claims
 * the analysis wants read first. Only bold and `code` are supported — the
 * dataset carries no other markup, and a full markdown renderer here would
 * happily interpret stray `#` or `-` inside Chinese prose as headings/lists. */

const TOKEN = /(\*\*[^*]+\*\*|`[^`]+`)/g;

export interface RichProps {
  text: string;
}

export function Rich({ text }: RichProps): JSX.Element {
  const parts = text.split(TOKEN).filter((p) => p !== "");
  return (
    <>
      {parts.map((part, i) => {
        if (part.startsWith("**") && part.endsWith("**")) {
          return <strong key={i}>{part.slice(2, -2)}</strong>;
        }
        if (part.startsWith("`") && part.endsWith("`")) {
          return <code key={i}>{part.slice(1, -1)}</code>;
        }
        return <span key={i}>{part}</span>;
      })}
    </>
  );
}
