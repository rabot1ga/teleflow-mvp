import clsx from 'clsx'
import type { ClassValue } from 'clsx'

/**
 * Utility function to merge class names
 * @param inputs - Class values to merge
 * @returns Merged class names
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}
