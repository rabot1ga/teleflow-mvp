/**
 * Get initials from a name string
 * @param name - Full name (e.g., "John Doe" or "john@example.com")
 * @returns Initials (e.g., "JD" or "J")
 */
export function getInitials(name: string): string {
  if (!name) return '?'
  
  const parts = name.trim().split(/\s+/)
  
  if (parts.length === 1) {
    // Single word - return first 2 characters or just the first character
    const word = parts[0]
    if (word.length >= 2) {
      return word.substring(0, 2).toUpperCase()
    }
    return word.charAt(0).toUpperCase()
  }
  
  // Multiple words - return first character of first and last word
  const first = parts[0]?.charAt(0) || ''
  const last = parts[parts.length - 1]?.charAt(0) || ''
  
  return (first + last).toUpperCase()
}
