// @ts-nocheck
export const validateEmail = (email: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
export const validatePassword = (pw: string) => pw.length >= 8 && /[A-Z]/.test(pw) && /[0-9]/.test(pw);
export const validateRequired = (val: unknown) => val !== null && val !== undefined && String(val).trim().length > 0;

export function validateForm(fields: Array<{ name: string; value: unknown; rules: Array<{ type: string; message?: string; value?: number }> }>) {
  const errors: Record<string, string> = {};
  for (const { name, value, rules } of fields) {
    for (const rule of rules) {
      if (rule.type === "required" && !validateRequired(value)) {
        errors[name] = rule.message || `${name} is required`;
        break;
      }
      if (rule.type === "email" && value && !validateEmail(value as string)) {
        errors[name] = rule.message || "Invalid email";
        break;
      }
      if (rule.type === "minLength" && value && typeof value === "string" && value.length < (rule.value ?? 0)) {
        errors[name] = rule.message || `Minimum ${rule.value} characters`;
        break;
      }
      if (rule.type === "password" && value && !validatePassword(value as string)) {
        errors[name] = rule.message || "Password must be 8+ chars with uppercase and a number";
        break;
      }
    }
  }
  return Object.keys(errors).length === 0 ? null : errors;
}
