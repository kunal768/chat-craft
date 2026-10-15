"use client"

import * as React from "react"
import { atom, useAtom } from "jotai"
import { X } from "lucide-react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

type ToastProps = {
  id: string
  title?: string
  description?: string
  action?: React.ReactNode
  variant?: "default" | "destructive" | "success"
}

const toastsAtom = atom<ToastProps[]>([])

export function useToast() {
  const [toasts, setToasts] = useAtom(toastsAtom)

  const toast = React.useCallback(
    ({ title, description, action, variant = "default" }: Omit<ToastProps, "id">) => {
      const id = Math.random().toString(36).substring(2, 9)
      setToasts((prev) => [...prev, { id, title, description, action, variant }])

      // Auto dismiss after 5 seconds
      setTimeout(() => {
        setToasts((prev) => prev.filter((toast) => toast.id !== id))
      }, 5000)

      return id
    },
    [setToasts],
  )

  const dismiss = React.useCallback(
    (id: string) => {
      setToasts((prev) => prev.filter((toast) => toast.id !== id))
    },
    [setToasts],
  )

  return {
    toast,
    dismiss,
    toasts,
  }
}

interface ToasterProps {
  className?: string
}

export function Toaster({ className }: ToasterProps) {
  const { toasts, dismiss } = useToast()

  return (
    <div className={cn("fixed bottom-4 right-4 z-50 flex flex-col gap-2", className)}>
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className={cn(
            "flex w-80 items-start gap-3 rounded-lg border p-4 shadow-lg",
            "bg-white dark:bg-slate-900",
            "animate-in slide-in-from-right-full",
            toast.variant === "destructive" && "border-red-500 bg-red-50 text-red-900 dark:bg-red-950 dark:text-red-50",
            toast.variant === "success" &&
              "border-green-500 bg-green-50 text-green-900 dark:bg-green-950 dark:text-green-50",
          )}
        >
          <div className="flex-1">
            {toast.title && <div className="font-semibold">{toast.title}</div>}
            {toast.description && <div className="text-sm opacity-90">{toast.description}</div>}
            {toast.action && <div className="mt-2">{toast.action}</div>}
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-6 w-6 rounded-full opacity-70 hover:opacity-100"
            onClick={() => dismiss(toast.id)}
          >
            <X className="h-4 w-4" />
            <span className="sr-only">Close</span>
          </Button>
        </div>
      ))}
    </div>
  )
}
