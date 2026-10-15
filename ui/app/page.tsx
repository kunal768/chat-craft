"use client"

import { Quote } from "@/components/ui/Quote"
import { Auth } from "@/components/Auth"


export default function Home() {
  // const [mounted, setMounted] = useState(false)

  // // Only show UI after first render to avoid hydration mismatch
  // useEffect(() => {
  //   setMounted(true)
  // }, [])

  // if (!mounted) {
  //   return null // Return nothing on first render
  // }

  return <div className="grid grid-cols-1 lg:grid-cols-3">
        <div className="col-span-1">
            <Auth type="signup" />
        </div>
        <div className="hidden lg:block col-span-2">
            <Quote/>
        </div>
    </div>
}
