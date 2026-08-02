export const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
export const validatePassword = (pw) => pw.length >= 8 && /[A-Z]/.test(pw) && /[0-9]/.test(pw);
export const validateRequired = (val) => val !== null && val !== undefined && String(val).trim().length > 0;

export function validateForm(fields) {
  const errors = {};
  for (const { name, value, rules } of fields) {
    for (const rule of rules) {
      if (rule.type === "required" && !validateRequired(value)) {
        errors[name] = rule.message || `${name} is required`;
        break;
      }
      if (rule.type === "email" && value && !validateEmail(value)) {
        errors[name] = rule.message || "Invalid email";
        break;
      }
      if (rule.type === "minLength" && value && value.length < rule.value) {
        errors[name] = rule.message || `Minimum ${rule.value} characters`;
        break;
      }
      if (rule.type === "password" && value && !validatePassword(value)) {
        errors[name] = rule.message || "Password must be 8+ chars with uppercase and a number";
        break;
      }
    }
  }
  return Object.keys(errors).length === 0 ? null : errors;
}
