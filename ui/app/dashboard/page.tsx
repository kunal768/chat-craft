"use client"

import { useEffect, useState } from "react"
import Dashboard from "@/components/dashboard"

export default function Home() {
  const [mounted, setMounted] = useState(false)

  // Only show UI after first render to avoid hydration mismatch
  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) {
    return null // Return nothing on first render
  }

  return  <Dashboard />


}
