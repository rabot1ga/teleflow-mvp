/**
 * TeleFlow WebSocket Service
 * Real-time updates for notifications, status changes, and analytics
 */

type WebSocketMessage = {
  type: 'notification' | 'status_update' | 'analytics_update' | 'article_created' | 'article_approved' | 'broadcast_started' | 'broadcast_completed' | 'pong' | 'connect' | 'disconnect' | 'ping'
  data: any
  timestamp: string
}

type WebSocketEventHandler = (message: WebSocketMessage) => void

// Export types
export type { WebSocketMessage, WebSocketEventHandler }

class WebSocketService {
  private ws: WebSocket | null = null
  private url: string
  private reconnectInterval: number = 3000
  private reconnectAttempts: number = 0
  private maxReconnectAttempts: number = 5
  private eventHandlers: Map<string, Set<WebSocketEventHandler>> = new Map()
  private heartbeatInterval: number = 30000
  private heartbeatTimer: NodeJS.Timeout | null = null

  constructor(url?: string) {
    this.url = url || (import.meta as any).env.VITE_WS_URL || 'ws://localhost/ws'
  }

  /**
   * Connect to WebSocket server
   */
  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(this.url)

        this.ws.onopen = () => {
          console.log('[WebSocket] Connected')
          this.reconnectAttempts = 0
          this.startHeartbeat()
          resolve()
        }

        this.ws.onclose = (event) => {
          console.log('[WebSocket] Disconnected', event.code, event.reason)
          this.stopHeartbeat()
          this.attemptReconnect()
        }

        this.ws.onerror = (error) => {
          console.error('[WebSocket] Error', error)
          reject(error)
        }

        this.ws.onmessage = (event) => {
          try {
            const message: WebSocketMessage = JSON.parse(event.data)
            this.handleMessage(message)
          } catch (error) {
            console.error('[WebSocket] Failed to parse message', error)
          }
        }
      } catch (error) {
        reject(error)
      }
    })
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close()
      this.ws = null
      this.stopHeartbeat()
      console.log('[WebSocket] Disconnected by client')
    }
  }

  /**
   * Subscribe to event type
   */
  on(eventType: string, handler: WebSocketEventHandler): () => void {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, new Set())
    }
    this.eventHandlers.get(eventType)!.add(handler)

    // Return unsubscribe function
    return () => {
      this.eventHandlers.get(eventType)?.delete(handler)
    }
  }

  /**
   * Send message to server
   */
  send(message: object): void {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    } else {
      console.warn('[WebSocket] Cannot send message, not connected')
    }
  }

  /**
   * Check if connected
   */
  isConnected(): boolean {
    return this.ws !== null && this.ws.readyState === WebSocket.OPEN
  }

  /**
   * Attempt to reconnect
   */
  private attemptReconnect(): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      console.log(`[WebSocket] Reconnecting... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`)
      setTimeout(() => this.connect(), this.reconnectInterval)
    } else {
      console.error('[WebSocket] Max reconnect attempts reached')
    }
  }

  /**
   * Start heartbeat to keep connection alive
   */
  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.isConnected()) {
        this.send({ type: 'ping', timestamp: new Date().toISOString() })
      }
    }, this.heartbeatInterval)
  }

  /**
   * Stop heartbeat
   */
  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
  }

  /**
   * Handle incoming message
   */
  private handleMessage(message: WebSocketMessage): void {
    // Handle pong response
    if ((message as any).type === 'pong') {
      return
    }

    // Notify all subscribers
    const handlers = this.eventHandlers.get(message.type)
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(message)
        } catch (error) {
          console.error('[WebSocket] Error in event handler', error)
        }
      })
    }

    // Also notify generic handler
    const genericHandlers = this.eventHandlers.get('*')
    if (genericHandlers) {
      genericHandlers.forEach(handler => handler(message))
    }
  }
}

// Singleton instance
let wsInstance: WebSocketService | null = null

export function getWebSocketService(): WebSocketService {
  if (!wsInstance) {
    wsInstance = new WebSocketService()
  }
  return wsInstance
}

export default WebSocketService
