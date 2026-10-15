"use client";

import { useState } from "react";
import { useTheme } from "next-themes";
import {
  Bot,
  BarChart3,
  FileText,
  Settings,
  Moon,
  Sun,
  Users,
  ChevronDown,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import ChatInterface from "@/components/chat-interface";
import ConfigPanel from "@/components/config-panel";

export default function Dashboard() {
  const { theme, setTheme } = useTheme();
  const [activeTab, setActiveTab] = useState("bot-management");

  return (
    <div className={`flex h-screen w-full overflow-hidden bg-slate-950 border-gray-800 `}>
      {/* Sidebar */}
      <aside className={`w-64 border-r border-gray-800  bg-slate-900 text-white flex flex-col`}>
        <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex items-center gap-2">
          <img src="./logo.png" className="h-10 w-10 text-blue-500" />
          <h1 className="text-xl font-bold">Chat-Craft</h1>
        </div>

        <nav className="flex-1 p-2">
          <ul className="space-y-1">
            {[
              { id: "bot-management", label: "Bot Management", icon: Bot },
              { id: "analytics", label: "Analytics", icon: BarChart3 },
              { id: "training-docs", label: "Training Docs", icon: FileText },
              { id: "settings", label: "Settings", icon: Settings },
            ].map((item) => (
              <li key={item.id}>
                <button
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm ${
                    activeTab === item.id
                      ? "bg-blue-500 text-white"
                      : "hover:bg-gray-100 dark:hover:bg-slate-800"
                  }`}
                >
                  <item.icon size={18} />
                  <span>{item.label}</span>
                </button>
              </li>
            ))}
          </ul>
        </nav>

        <div className="p-4 border-t border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Users size={18} />
              <span className="text-sm">Team Workspace</span>
            </div>
            <Button
              variant="ghost"
              size="icon"
              //onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            >
              {theme === "dark" ? (
                <Sun size={18} />
              ) : (
                <Moon className="text-white" size={18} />
              )}
            </Button>
          </div>
        </div>
      </aside> 

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-14 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between px-4">
          <div className="flex items-center gap-4">
            {/* Dropdown Menu */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" className="flex items-center gap-2">
                  <span>Customer Support Bot</span>
                  <ChevronDown size={16} />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="start">
                {["Customer Support Bot", "Sales Assistant", "Technical Support"].map(
                  (item) => (
                    <DropdownMenuItem key={item}>{item}</DropdownMenuItem>
                  )
                )}
              </DropdownMenuContent>
            </DropdownMenu>

            {/* Status */}
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 rounded-full bg-green-500"></div>
              <span className="text-sm text-gray-500 dark:text-gray-400">Active</span>
            </div>
          </div>
        </header>

        {/* Content */}
        <section className="flex-1 overflow-hidden">
          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="h-full">
            {/* Tab Content */}
            <TabsContent value={activeTab} className="h-full m-0 p-0">
              {/* Split View */}
              <div className="flex h-full">
                {/* Chat Interface */}
                <div className="w-[70%] border-r border-gray-200 dark:border-gray-800">
                  <ChatInterface />
                </div>

                {/* Config Panel */}
                <div className="w-[30%]">
                  <ConfigPanel activeTab={activeTab} />
                </div>
              </div>
            </TabsContent>
          </Tabs>
        </section>
      </main>
    </div>
  );
}
