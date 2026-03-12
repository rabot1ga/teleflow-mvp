import { useQuery, useMutation, useQueryClient, type UseQueryOptions, type UseMutationOptions } from '@tanstack/react-query'
import toast from 'react-hot-toast'

interface UseApiQueryOptions<T> extends Omit<UseQueryOptions<T>, 'queryKey' | 'queryFn'> {
  queryKeySuffix?: string
  enabled?: boolean
}

export function useApiQuery<T>(
  key: string,
  fetcher: () => Promise<T>,
  options?: UseApiQueryOptions<T>
) {
  return useQuery({
    queryKey: [key, ...(options?.queryKeySuffix ? [options.queryKeySuffix] : [])],
    queryFn: fetcher,
    retry: 1,
    refetchOnWindowFocus: false,
    ...options,
  })
}

interface UseApiMutationOptions<TData, TError, TVariables> extends Omit<UseMutationOptions<TData, TError, TVariables>, 'mutationKey' | 'onSuccess' | 'onError'> {
  successMessage?: string
  errorMessage?: string
  invalidateKeys?: string[]
}

export function useApiMutation<TData = unknown, TError = unknown, TVariables = void>(
  key: string,
  mutationFn: (variables: TVariables) => Promise<TData>,
  options?: UseApiMutationOptions<TData, TError, TVariables>
) {
  const queryClient = useQueryClient()
  
  return useMutation({
    mutationKey: [key],
    mutationFn,
    onSuccess: (_data: any, _variables: any, _context: any) => {
      // Show success toast
      if (options?.successMessage) {
        toast.success(options.successMessage)
      }

      // Invalidate queries
      if (options?.invalidateKeys) {
        options.invalidateKeys.forEach((queryKey) => {
          queryClient.invalidateQueries({ queryKey: [queryKey] })
        })
      }
    },
    onError: (error: any, _variables: any, _context: any) => {
      // Show error toast
      const errorMessage = options?.errorMessage ||
        (error instanceof Error ? error.message : 'An error occurred')
      toast.error(errorMessage)
    },
  })
}

// Pre-built hooks for common operations
export function useCreate<TData, TVariables>(
  resource: string,
  createFn: (variables: TVariables) => Promise<TData>,
  options?: Omit<UseApiMutationOptions<TData, Error, TVariables>, 'successMessage'>
) {
  return useApiMutation(
    `create-${resource}`,
    createFn,
    {
      successMessage: `${resource} created successfully`,
      invalidateKeys: [resource],
      ...options,
    }
  )
}

export function useUpdate<TData, TVariables>(
  resource: string,
  updateFn: (variables: TVariables) => Promise<TData>,
  options?: Omit<UseApiMutationOptions<TData, Error, TVariables>, 'successMessage'>
) {
  return useApiMutation(
    `update-${resource}`,
    updateFn,
    {
      successMessage: `${resource} updated successfully`,
      invalidateKeys: [resource],
      ...options,
    }
  )
}

export function useDelete<TVariables = string>(
  resource: string,
  deleteFn: (id: TVariables) => Promise<void>,
  options?: Omit<UseApiMutationOptions<void, Error, TVariables>, 'successMessage'>
) {
  return useApiMutation(
    `delete-${resource}`,
    deleteFn,
    {
      successMessage: `${resource} deleted successfully`,
      invalidateKeys: [resource],
      ...options,
    }
  )
}
