import { useState, useEffect, useRef } from 'react'
import { getWebSocketService } from '@/services/websocket'
import type { WebSocketMessage } from '@/services/websocket'

interface UseWebSocketOptions {
  onConnect?: () => void
  onDisconnect?: () => void
  onError?: (error: any) => void
  reconnect?: boolean
}

/**
 * Hook for using WebSocket in React components
 * 
 * @param eventType - Event type to subscribe to (or '*' for all events)
 * @param handler - Callback function for handling messages
 * @param options - Additional options
 * 
 * @example
 * ```tsx
 * function Notifications() {
 *   useWebSocket('notification', (message) => {
 *     toast.success(message.data.message)
 *   })
 * 
 *   return <div>...</div>
 * }
 * ```
 */
export function useWebSocket(
  eventType: string,
  handler: (message: WebSocketMessage) => void,
  options: UseWebSocketOptions = {}
): void {
  const { onConnect, onDisconnect, onError, reconnect = true } = options
  const wsService = useRef(getWebSocketService())
  const handlerRef = useRef(handler)

  // Update handler ref when it changes
  useEffect(() => {
    handlerRef.current = handler
  }, [handler])

  useEffect(() => {
    const ws = wsService.current

    // Connect on mount
    ws.connect()
      .then(() => {
        onConnect?.()
      })
      .catch((error) => {
        onError?.(error)
      })

    // Subscribe to events
    const unsubscribe = ws.on(eventType, (message) => {
      handlerRef.current(message)
    })

    // Handle connection state changes
    const handleDisconnect = () => {
      if (reconnect) {
        // Will auto-reconnect
      } else {
        onDisconnect?.()
      }
    }

    // Subscribe to disconnect event
    const unsubscribeDisconnect = ws.on('*', (message: WebSocketMessage) => {
      if ((message as any).type === 'disconnect') {
        handleDisconnect()
      }
    })

    // Cleanup on unmount
    return () => {
      unsubscribe()
      unsubscribeDisconnect()
      if (!reconnect) {
        ws.disconnect()
      }
    }
  }, [eventType, onConnect, onDisconnect, onError, reconnect])
}

/**
 * Hook for subscribing to multiple event types
 * 
 * @example
 * ```tsx
 * function Dashboard() {
 *   useWebSocketMulti({
 *     'notification': (msg) => toast.success(msg.data.message),
 *     'analytics_update': (msg) => updateStats(msg.data),
 *     'article_approved': (msg) => refetchArticles()
 *   })
 * 
 *   return <div>...</div>
 * }
 * ```
 */
export function useWebSocketMulti(
  eventHandlers: Record<string, (message: WebSocketMessage) => void>,
  options: UseWebSocketOptions = {}
): void {
  const wsService = useRef(getWebSocketService())

  useEffect(() => {
    const ws = wsService.current

    ws.connect()
      .then(() => {
        options.onConnect?.()
      })
      .catch((error) => {
        options.onError?.(error)
      })

    // Subscribe to all event types
    const unsubscribers: Array<() => void> = []

    Object.entries(eventHandlers).forEach(([eventType, handler]) => {
      const unsubscribe = ws.on(eventType, handler)
      unsubscribers.push(unsubscribe)
    })

    // Cleanup
    return () => {
      unsubscribers.forEach(unsubscribe => unsubscribe())
      if (!options.reconnect) {
        ws.disconnect()
      }
    }
  }, [JSON.stringify(eventHandlers), options.onConnect, options.onError, options.reconnect])
}

/**
 * Hook for checking WebSocket connection status
 */
export function useWebSocketStatus(): { isConnected: boolean; isConnecting: boolean } {
  const wsService = useRef(getWebSocketService())
  const [isConnected, setIsConnected] = useState(wsService.current.isConnected())
  const [isConnecting, setIsConnecting] = useState(false)

  useEffect(() => {
    const ws = wsService.current

    // Subscribe to connection state changes
    const unsubscribe = ws.on('*', (message: WebSocketMessage) => {
      if ((message as any).type === 'connect') {
        setIsConnected(true)
        setIsConnecting(false)
      } else if ((message as any).type === 'disconnect') {
        setIsConnected(false)
      }
    })

    // Check connection status periodically
    const interval = setInterval(() => {
      setIsConnected(ws.isConnected())
    }, 1000)

    return () => {
      unsubscribe()
      clearInterval(interval)
    }
  }, [])

  return { isConnected, isConnecting }
}
