"use client"

import type React from "react"

import { useState, useEffect, useRef  } from "react"
import { FileText, Upload, Check, Clock, RefreshCw, Shield, Bot, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Slider } from "@/components/ui/slider"
import { Switch } from "@/components/ui/switch"
import axios from "axios";

import { useToast } from "@/components/ui/use-toast"

type ConfigPanelProps = {
  activeTab: string
}

type DocType = {
  id: number
  name: string
  status: string
  progress?: number
  version: number
  type?: string
  size?: string
  date?: string
}

export default function ConfigPanel({ activeTab }: ConfigPanelProps) {
  const [activeConfigTab, setActiveConfigTab] = useState("docs")
  const [primaryColor, setPrimaryColor] = useState("#2563EB")
  const [uploadedDocs, setUploadedDocs] = useState<DocType[]>([])
  const [apiKey, setApiKey] = useState("**************************");

  const [isDragging, setIsDragging] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const { toast } = useToast()

  // Initialize data on client-side only
  useEffect(() => {
    setUploadedDocs([
      {
        id: 1,
        name: "Product Manual.pdf",
        status: "trained",
        version: 3,
        type: "PDF",
        size: "2.4 MB",
        date: "2023-04-10",
      },
      {
        id: 2,
        name: "API Documentation.pdf",
        status: "trained",
        version: 1,
        type: "PDF",
        size: "3.2 MB",
        date: "2023-04-07",
      },
      {
        id: 3,
        name: "User Guide.docx",
        status: "trained",
        version: 2,
        type: "Word",
        size: "1.5 MB",
        date: "2023-04-06",
      },
    ])
  }, [])

  const handleBrowseFiles = () => {
    fileInputRef.current?.click()
  }
  
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFiles(Array.from(files))
    }
  }
  
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }
  
  const handleDragLeave = () => {
    setIsDragging(false)
  }
  
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFiles(Array.from(e.dataTransfer.files))
    }
  }
  
  const handleFiles = (files: File[]) => {
    const newDocs: DocType[] = files.map((file, index) => {
      const fileType = getFileType(file.name)
      return {
        id: Date.now() + index,
        name: file.name,
        status: "queued",
        version: 1,
        type: fileType,
        size: formatFileSize(file.size),
        date: new Date().toISOString().split("T")[0],
      }
    })
  
    setUploadedDocs((prev) => [...newDocs, ...prev])
  
    toast({
      title: "Files queued for upload",
      description: `${files.length} file(s) have been queued.`,
      variant: "success",
    })
  
    files.forEach((file, idx) => {
      uploadFile({
        file,
        docId: newDocs[idx].id,
        userId: "67f2cedfe24b7b94d496ebb4", // TODO: Replace with actual user id
        docName: file.name,
        docType: getFileType(file.name),
        docUrl: "your-doc-url", // TODO: Replace with actual doc url (if needed)
        updateInterval: "-1" // or "" or undefined if not needed
      })
    })
  }
  
  const uploadFile = async ({
    file,
    docId,
    userId,
    docName,
    docType,
    docUrl,
    updateInterval
  }: {
    file: File
    docId: number
    userId: string
    docName: string
    docType?: string
    docUrl: string
    updateInterval?: string
  }) => {
    const formData = new FormData()
    formData.append("user_id", userId)
    formData.append("doc_name", docName)
    if (docType) formData.append("doc_type", docType)
    formData.append("doc_url", docUrl)
    if (updateInterval) formData.append("update_interval", updateInterval)
    formData.append("file", file)
  
    try {
      await axios.post(
        "http://10.251.75.84:8000/v1/upload/file",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data", "x-api-key" : "entities-api-key" }
        }
      )
      setUploadedDocs((prev) =>
        prev.map((doc) =>
          doc.id === docId ? { ...doc, status: "uploaded" } : doc
        )
      )
      toast({
        title: "File uploaded",
        description: `${file.name} uploaded successfully.`,
        variant: "success",
      })
    } catch (error) {
      setUploadedDocs((prev) =>
        prev.map((doc) =>
          doc.id === docId ? { ...doc, status: "error" } : doc
        )
      )
      toast({
        title: "Upload failed",
        description: `Failed to upload ${file.name}`,
        variant: "destructive",
      })
    }
  }

  const getFileType = (filename: string) => {
    const extension = filename.split(".").pop()?.toLowerCase()
    switch (extension) {
      case "pdf":
        return "PDF"
      case "doc":
      case "docx":
        return "Word"
      case "xls":
      case "xlsx":
        return "Excel"
      case "ppt":
      case "pptx":
        return "PowerPoint"
      case "txt":
        return "Text"
      default:
        return extension?.toUpperCase() || "Unknown"
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + " B"
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB"
    else return (bytes / 1048576).toFixed(1) + " MB"
  }

  const removeDocument = (id: number) => {
    setUploadedDocs((prev) => prev.filter((doc) => doc.id !== id))
  }

  return (
    <div className="h-full overflow-auto">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-white mb-4">Configuration Panel</h2>

        {activeTab === "bot-management" && (
          <Tabs defaultValue="docs" value={activeConfigTab} onValueChange={setActiveConfigTab}>
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="docs">Documents</TabsTrigger>
              <TabsTrigger value="brand">Branding</TabsTrigger>
              <TabsTrigger value="behavior">Behavior</TabsTrigger>
            </TabsList>

            <TabsContent value="docs" className="space-y-4 mt-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Document Training</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className={`rounded-lg border-2 border-dashed border-gray-200 dark:border-gray-800 p-6 text-center 
                    ${isDragging ? "border-primary bg-primary/5" : ""}`}
                    onDragOver={handleDragOver}
                    onDragLeave={handleDragLeave}
                    onDrop={handleDrop}
                    >
                    <Upload className="mx-auto h-8 w-8 text-gray-400" />
                    <p className="mt-2 text-sm font-medium">Drag and drop files or</p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">Supports Google Docs, Sheets, PDFs, and more</p>
                    <Button size="sm" variant="secondary" className="mt-2 cursor-pointer" onClick={handleBrowseFiles}>
                      Browse Files
                    </Button>
                    <input
                      type="file"
                      ref={fileInputRef}
                      className="hidden"
                      multiple
                      onChange={handleFileChange}
                      accept=".pdf,.doc,.docx,.xls,.xlsx,.csv"
                    />
                  </div>

                  <div className="mt-4 space-y-3">
                    {uploadedDocs.slice(0, 5).map((doc) => (
                      <div key={doc.id} className="flex items-center justify-between rounded-lg border border-gray-200 dark:border-gray-800 p-2">
                        <div className="flex items-center gap-2">
                          <FileText className="h-4 w-4 text-gray-400" />
                          <div>
                            <p className="text-sm font-medium">{doc.name}</p>
                            <p className="text-xs text-gray-500">{doc.type} • {doc.size} • v{doc.version}</p>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {doc.status === "queued" ? (
                            <div className="flex items-center gap-1 text-amber-500">
                              <Clock className="h-4 w-4" />
                              <span className="text-xs">Queued</span>
                            </div>
                          ) : doc.status === "training" ? (
                            <div className="w-24">
                              <Progress value={doc.progress} className="h-2" />
                              <p className="text-xs text-gray-500 dark:text-gray-400 text-right mt-1">{doc.progress}%</p>
                            </div>
                          ) : (
                            <div className="flex items-center gap-1 text-green-500">
                            <Check className="h-4 w-4" />
                            <span className="text-xs">Trained</span>
                          </div>
                          )}
                          <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 text-gray-400 hover:text-red-500"
                          onClick={() => removeDocument(doc.id)}
                          >
                          <X className="h-3 w-3" />
                        </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Training Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="auto-train">Auto-train on upload</Label>
                    <Switch id="auto-train" defaultChecked />
                  </div>
                  <div className="flex items-center justify-between">
                    <Label htmlFor="version-control">Enable version control</Label>
                    <Switch id="version-control" defaultChecked />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="chunk-size">Chunk Size</Label>
                    <Select defaultValue="medium">
                      <SelectTrigger id="chunk-size">
                        <SelectValue placeholder="Select chunk size" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="small">Small (better for specific answers)</SelectItem>
                        <SelectItem value="medium">Medium (balanced)</SelectItem>
                        <SelectItem value="large">Large (better for context)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="brand" className="space-y-4 mt-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Brand Customization</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="bot-name">Bot Name</Label>
                    <Input id="bot-name" defaultValue="Customer Support Bot" />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="primary-color">Primary Color</Label>
                    <div className="flex items-center gap-2">
                      <Input
                        type="color"
                        id="primary-color"
                        value={primaryColor}
                        onChange={(e) => setPrimaryColor(e.target.value)}
                        className="w-12 h-8 p-1"
                      />
                      <Input
                        type="text"
                        value={primaryColor}
                        onChange={(e) => setPrimaryColor(e.target.value)}
                        className="flex-1"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="bot-avatar">Bot Avatar</Label>
                    <div className="flex items-center gap-2">
                      <div className="h-10 w-10 rounded-full bg-primary flex items-center justify-center text-white">
                        <Bot className="h-6 w-6" />
                      </div>
                      <Button variant="outline" size="sm">
                        Upload Logo
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="tone">Conversation Tone</Label>
                    <Select defaultValue="professional">
                      <SelectTrigger id="tone">
                        <SelectValue placeholder="Select tone" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="professional">Professional</SelectItem>
                        <SelectItem value="casual">Casual</SelectItem>
                        <SelectItem value="technical">Technical</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="pt-2">
                    <Button className="w-full">Save Brand Settings</Button>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Compliance</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    <div className="flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-xs text-blue-800 dark:bg-blue-900 dark:text-blue-100">
                      <Shield className="h-3 w-3" />
                      <span>GDPR Compliant</span>
                    </div>
                    <div className="flex items-center gap-1 rounded-full bg-green-100 px-3 py-1 text-xs text-green-800 dark:bg-green-900 dark:text-green-100">
                      <Shield className="h-3 w-3" />
                      <span>ADA Compliant</span>
                    </div>
                    <div className="flex items-center gap-1 rounded-full bg-purple-100 px-3 py-1 text-xs text-purple-800 dark:bg-purple-900 dark:text-purple-100">
                      <Shield className="h-3 w-3" />
                      <span>HIPAA Ready</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="behavior" className="space-y-4 mt-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Response Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="response-length">Response Length</Label>
                      <span className="text-xs text-gray-500 dark:text-gray-400">Medium</span>
                    </div>
                    <Slider defaultValue={[50]} max={100} step={1} className="w-full" />
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Label htmlFor="creativity">Creativity</Label>
                      <span className="text-xs text-gray-500 dark:text-gray-400">Balanced</span>
                    </div>
                    <Slider defaultValue={[60]} max={100} step={1} className="w-full" />
                  </div>

                  <div className="flex items-center justify-between">
                    <Label htmlFor="quick-replies">Enable Quick Replies</Label>
                    <Switch id="quick-replies" defaultChecked />
                  </div>

                  <div className="flex items-center justify-between">
                    <Label htmlFor="feedback">Enable Feedback Buttons</Label>
                    <Switch id="feedback" defaultChecked />
                  </div>

                  <div className="flex items-center justify-between">
                    <Label htmlFor="typing-indicator">Show Typing Indicator</Label>
                    <Switch id="typing-indicator" defaultChecked />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Advanced Settings</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="model">AI Model</Label>
                    <Select defaultValue="gpt4">
                      <SelectTrigger id="model">
                        <SelectValue placeholder="Select model" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="gpt4">GPT-4o</SelectItem>
                        <SelectItem value="gpt35">GPT-3.5 Turbo</SelectItem>
                        <SelectItem value="claude">Claude 3 Opus</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center justify-between">
                    <Label htmlFor="memory">Conversation Memory</Label>
                    <Switch id="memory" defaultChecked />
                  </div>

                  <div className="flex items-center justify-between">
                    <Label htmlFor="fallback">Enable Fallback Responses</Label>
                    <Switch id="fallback" defaultChecked />
                  </div>

                  <div className="pt-2">
                    <Button variant="outline" className="w-full">
                      <RefreshCw className="mr-2 h-4 w-4" />
                      Reset to Defaults
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        )}

        {activeTab === "analytics" && (
          <div className="space-y-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Performance Overview</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-3 gap-4">
                    <div className="rounded-lg border border-gray-200 dark:border-gray-800 p-3">
                      <div className="text-xs text-gray-500 dark:text-gray-400">Avg. Response Time</div>
                      <div className="text-2xl font-bold">1.8s</div>
                      <div className="text-xs text-green-500">↓ 12% from last week</div>
                    </div>
                    <div className="rounded-lg border border-gray-200 dark:border-gray-800 p-3">
                      <div className="text-xs text-gray-500 dark:text-gray-400">Resolution Rate</div>
                      <div className="text-2xl font-bold">87%</div>
                      <div className="text-xs text-green-500">↑ 5% from last week</div>
                    </div>
                    <div className="rounded-lg border border-gray-200 dark:border-gray-800 p-3">
                      <div className="text-xs text-gray-500 dark:text-gray-400">User Satisfaction</div>
                      <div className="text-2xl font-bold">4.7/5</div>
                      <div className="text-xs text-green-500">↑ 0.3 from last week</div>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-sm font-medium mb-2">User Sentiment Trend</h3>
                    <div className="h-[200px] w-full rounded-lg border border-gray-200 dark:border-gray-800 p-4">
                      {/* Sentiment graph would go here */}
                      <div className="flex h-full items-end gap-2">
                        {[35, 45, 38, 52, 48, 60, 70, 65, 75].map((value, i) => (
                          <div key={i} className="flex-1 bg-blue-600 rounded-t" style={{ height: `${value}%` }} />
                        ))}
                      </div>
                      <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
                        <span>Mon</span>
                        <span>Tue</span>
                        <span>Wed</span>
                        <span>Thu</span>
                        <span>Fri</span>
                        <span>Sat</span>
                        <span>Sun</span>
                        <span>Mon</span>
                        <span>Tue</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Top Queries</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    {[
                      { query: "How do I reset my password?", count: 127 },
                      { query: "What are your pricing plans?", count: 98 },
                      { query: "How to integrate with my website?", count: 76 },
                      { query: "Do you offer refunds?", count: 62 },
                      { query: "How to train custom documents?", count: 54 },
                    ].map((item, i) => (
                      <div key={i} className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <div className="flex h-6 w-6 items-center justify-center rounded-full bg-gray-100 dark:bg-gray-800 text-xs font-medium">
                            {i + 1}
                          </div>
                          <span className="text-sm">{item.query}</span>
                        </div>
                        <div className="text-sm text-gray-500 dark:text-gray-400">{item.count}</div>
                      </div>
                    ))}
                  </div>

                  <Button variant="outline" className="w-full text-xs">
                    View All Queries
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === "training-docs" && (
          <div className="space-y-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Document Management</CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`rounded-lg border-2 border-dashed border-gray-200 dark:border-gray-800 p-6 text-center 
                  ${isDragging ? "border-blue-600 bg-blue-600" : ""}
                  `}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  >
                  <Upload className="mx-auto h-8 w-8 text-gray-400" />
                  <p className="mt-2 text-sm font-medium">Drag and drop files or</p>
                  <p className="text-xs text-muted-foreground">Supports Google Docs, Sheets, PDFs, and more</p>
                  <Button size="sm" variant="secondary" className="mt-2" onClick={handleBrowseFiles}>
                    Browse Files
                  </Button>
                </div>

                <div className="mt-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="text-sm font-medium">Uploaded Documents</h3>
                    <Select defaultValue="all">
                      <SelectTrigger className="h-8 w-[120px]">
                        <SelectValue placeholder="Filter" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">All Documents</SelectItem>
                        <SelectItem value="trained">Trained</SelectItem>
                        <SelectItem value="pending">Pending</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    {uploadedDocs.map((doc, i) => (
                      <div key={i} className="flex items-center justify-between rounded-lg border border-gray-200 border-gray-800 p-2">
                        <div className="flex items-center gap-2">
                          <FileText className="h-4 w-4 text-muted-foreground" />
                          <div>
                            <p className="text-sm font-medium">{doc.name}</p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">
                              {doc.type} • {doc.size}
                            </p>
                          </div>
                        </div>
                        <div className="flex items-center gap-4">
                          <p className="text-xs text-gray-500 dark:text-gray-400">{doc.date}</p>
                          {doc.status === "trained" ? (
                            <div className="flex items-center gap-1 text-green-500">
                              <Check className="h-4 w-4" />
                              <span className="text-xs">Trained</span>
                            </div>
                          ) : doc.status === "training" ? (
                            <div className="flex items-center gap-1 text-blue-500">
                              <RefreshCw className="h-4 w-4 animate-spin" />
                              <span className="text-xs">Training</span>
                            </div>
                          ) : (
                            <div className="flex items-center gap-1 text-amber-500">
                              <Clock className="h-4 w-4" />
                              <span className="text-xs">Queued</span>
                            </div>
                          )}
                          <Button 
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 text-gray-400 hover:text-red-500"
                          onClick={() => removeDocument(doc.id)}                         
                          >
                            <X className="h-3 w-3"/>
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Training Configuration</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="embedding-model">Embedding Model</Label>
                  <Select defaultValue="openai">
                    <SelectTrigger id="embedding-model">
                      <SelectValue placeholder="Select model" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="openai">OpenAI Embeddings</SelectItem>
                      <SelectItem value="cohere">Cohere Embeddings</SelectItem>
                      <SelectItem value="custom">Custom Embeddings</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="chunk-strategy">Chunking Strategy</Label>
                  <Select defaultValue="paragraph">
                    <SelectTrigger id="chunk-strategy">
                      <SelectValue placeholder="Select strategy" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="paragraph">Paragraph</SelectItem>
                      <SelectItem value="fixed">Fixed Size</SelectItem>
                      <SelectItem value="semantic">Semantic</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="flex items-center justify-between">
                  <Label htmlFor="auto-retrain">Auto-retrain on updates</Label>
                  <Switch id="auto-retrain" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <Label htmlFor="version-history">Keep version history</Label>
                  <Switch id="version-history" defaultChecked />
                </div>

                <Button className="w-full">Save Configuration</Button>
              </CardContent>
            </Card>
          </div>
        )}

        {activeTab === "settings" && (
          <div className="space-y-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">General Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="bot-name-settings">Bot Name</Label>
                  <Input id="bot-name-settings" defaultValue="Customer Support Bot" />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="description">Description</Label>
                  <Input id="description" defaultValue="AI assistant for customer support inquiries" />
                </div>

                <div className="flex items-center justify-between">
                  <Label htmlFor="active-status">Active Status</Label>
                  <Switch id="active-status" defaultChecked />
                </div>

                <div className="flex items-center justify-between">
                  <Label htmlFor="public-access">Public Access</Label>
                  <Switch id="public-access" />
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Integration Settings</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="api-key">API Key</Label>
                  <div className="flex gap-2">
                    <Input id="api-key" type="password" value={apiKey} readOnly />
                    <Button variant="outline" size="icon">
                      <RefreshCw className="h-4 w-4" />
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground">Use this key to access your bot via API</p>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="webhook">Webhook URL</Label>
                  <Input id="webhook" placeholder="https://your-app.com/webhook" />
                </div>

                <div className="rounded-lg border border-gray-200 border-gray-800 p-3">
                  <div className="flex items-center gap-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300">
                      <Check className="h-4 w-4" />
                    </div>
                    <div>
                      <p className="text-sm font-medium">Website Widget</p>
                      <p className="text-xs text-muted-foreground">Connected to yourdomain.com</p>
                    </div>
                  </div>
                  <Button variant="link" className="mt-2 h-auto p-0 text-xs">
                    Configure Widget
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium">Team Access</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {[
                    { name: "Nikhil", email: "nikhil@example.com", role: "Admin" },
                    { name: "Kunal", email: "kunal@example.com", role: "Editor" },
                    { name: "Kenil", email: "kenil@example.com", role: "Viewer" },
                    { name: "Deven", email: "deven@example.com", role: "Viewer" },
                    { name: "Muqtadir", email: "muqtadir@example.com", role: "Viewer" },
                  ].map((user, i) => (
                    <div key={i} className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-white">
                          {user.name
                            .split(" ")
                            .map((n) => n[0])
                            .join("")}
                        </div>
                        <div>
                          <p className="text-sm font-medium">{user.name}</p>
                          <p className="text-xs text-muted-foreground">{user.email}</p>
                        </div>
                      </div>
                      <Select defaultValue={user.role.toLowerCase()}>
                        <SelectTrigger className="h-8 w-[100px]">
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="admin">Admin</SelectItem>
                          <SelectItem value="editor">Editor</SelectItem>
                          <SelectItem value="viewer">Viewer</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  ))}
                </div>

                <Button variant="outline" className="mt-4 w-full text-xs">
                  Invite Team Member
                </Button>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}
