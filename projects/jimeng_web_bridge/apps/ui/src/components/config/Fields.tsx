import { type ReactNode, useId, useState } from "react";

export interface FieldProps {
  path: string;
  label: string;
  hint?: string | null;
  error?: string | null;
  readOnlyReason?: string | null;
}

function useFieldIds() {
  const id = useId();
  return { input: `${id}-input`, hint: `${id}-hint`, error: `${id}-error`, readOnly: `${id}-ro` };
}

type FieldIds = ReturnType<typeof useFieldIds>;

function describedBy(ids: FieldIds, props: FieldProps): string | undefined {
  const parts = [props.hint ? ids.hint : null, props.readOnlyReason ? ids.readOnly : null, props.error ? ids.error : null].filter(Boolean);
  return parts.length ? parts.join(" ") : undefined;
}

function FieldNotes({ ids, props }: { ids: FieldIds; props: FieldProps }) {
  return (
    <>
      {props.hint ? (
        <span id={ids.hint} className="field-hint">
          {props.hint}
        </span>
      ) : null}
      {props.readOnlyReason ? (
        <span id={ids.readOnly} className="field-hint">
          <span aria-hidden="true">🔒 </span>
          {props.readOnlyReason}
        </span>
      ) : null}
      {props.error ? (
        <span id={ids.error} className="field-error">
          错误：{props.error}
        </span>
      ) : null}
    </>
  );
}

function FieldLabel({ htmlFor, props }: { htmlFor: string; props: FieldProps }): ReactNode {
  return (
    <label htmlFor={htmlFor}>
      {props.label} <code>{props.path}</code>
    </label>
  );
}

function display(value: unknown): string {
  if (value === undefined || value === null) return "";
  return typeof value === "string" ? value : String(value);
}

export function TextField(props: FieldProps & { value: unknown; onChange: (value: string) => void }) {
  const ids = useFieldIds();
  return (
    <div className="field">
      <FieldLabel htmlFor={ids.input} props={props} />
      <input
        id={ids.input}
        type="text"
        value={display(props.value)}
        readOnly={Boolean(props.readOnlyReason)}
        aria-invalid={props.error ? true : undefined}
        aria-describedby={describedBy(ids, props)}
        data-config-key={props.path}
        onChange={(event) => props.onChange(event.target.value)}
      />
      <FieldNotes ids={ids} props={props} />
    </div>
  );
}

export function NumberField(props: FieldProps & { value: unknown; onChange: (value: number | string) => void }) {
  const ids = useFieldIds();
  return (
    <div className="field">
      <FieldLabel htmlFor={ids.input} props={props} />
      <input
        id={ids.input}
        type="text"
        inputMode="decimal"
        value={display(props.value)}
        readOnly={Boolean(props.readOnlyReason)}
        aria-invalid={props.error ? true : undefined}
        aria-describedby={describedBy(ids, props)}
        data-config-key={props.path}
        onChange={(event) => {
          const raw = event.target.value;
          const parsed = Number(raw);
          props.onChange(raw.trim() !== "" && Number.isFinite(parsed) ? parsed : raw);
        }}
      />
      <FieldNotes ids={ids} props={props} />
    </div>
  );
}

export function SelectField(props: FieldProps & { value: unknown; options: readonly string[]; onChange: (value: string) => void }) {
  const ids = useFieldIds();
  const current = display(props.value);
  const options = current && !props.options.includes(current) ? [current, ...props.options] : props.options;
  return (
    <div className="field">
      <FieldLabel htmlFor={ids.input} props={props} />
      <select
        id={ids.input}
        value={current}
        disabled={Boolean(props.readOnlyReason)}
        aria-invalid={props.error ? true : undefined}
        aria-describedby={describedBy(ids, props)}
        data-config-key={props.path}
        onChange={(event) => props.onChange(event.target.value)}
      >
        {current === "" ? <option value="">（未设置）</option> : null}
        {options.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
      <FieldNotes ids={ids} props={props} />
    </div>
  );
}

export function CheckboxField(props: FieldProps & { value: unknown; onChange: (value: boolean) => void }) {
  const ids = useFieldIds();
  return (
    <div className="field">
      <label htmlFor={ids.input}>
        <input
          id={ids.input}
          type="checkbox"
          checked={props.value === true}
          disabled={Boolean(props.readOnlyReason)}
          aria-invalid={props.error ? true : undefined}
          aria-describedby={describedBy(ids, props)}
          data-config-key={props.path}
          onChange={(event) => props.onChange(event.target.checked)}
        />{" "}
        {props.label} <code>{props.path}</code>
      </label>
      <FieldNotes ids={ids} props={props} />
    </div>
  );
}

export function ListField(props: FieldProps & { value: unknown; onChange: (value: string[]) => void }) {
  const ids = useFieldIds();
  const [text, setText] = useState(() => (Array.isArray(props.value) ? props.value.map((item) => String(item)).join("\n") : ""));
  return (
    <div className="field">
      <FieldLabel htmlFor={ids.input} props={props} />
      <textarea
        id={ids.input}
        rows={3}
        value={text}
        readOnly={Boolean(props.readOnlyReason)}
        aria-invalid={props.error ? true : undefined}
        aria-describedby={describedBy(ids, props)}
        data-config-key={props.path}
        onChange={(event) => {
          setText(event.target.value);
          props.onChange(
            event.target.value
              .split("\n")
              .map((line) => line.trim())
              .filter(Boolean),
          );
        }}
      />
      <FieldNotes ids={ids} props={{ ...props, hint: props.hint ?? "每行一项" }} />
    </div>
  );
}
