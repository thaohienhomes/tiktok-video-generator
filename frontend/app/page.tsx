'use client'

import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, Globe, Settings, Play, Download, CheckCircle, AlertCircle } from 'lucide-react'
import { apiHelpers } from '../lib/api'

type ProcessingStatus = 'idle' | 'uploading' | 'processing' | 'completed' | 'error'

interface ProcessingJob {
  status: string
  progress: number
  message: string
  result?: {
    video_path: string
    script: string
    category: string
    marketing: {
      caption: string
      hashtags: string[]
      description: string
      hook: string
    }
  }
  error?: string
}

export default function HomePage() {
  const [status, setStatus] = useState<ProcessingStatus>('idle')
  const [jobId, setJobId] = useState<string>('')
  const [progress, setProgress] = useState(0)
  const [message, setMessage] = useState('')
  const [result, setResult] = useState<ProcessingJob['result'] | null>(null)
  const [error, setError] = useState('')
  
  // Form state
  const [url, setUrl] = useState('')
  const [duration, setDuration] = useState(180)
  const [voiceStyle, setVoiceStyle] = useState('professional')
  const [inputType, setInputType] = useState<'file' | 'url'>('file')

  const handleUploadFile = async (files: File[]) => {
    if (files.length === 0) return
    
    const file = files[0]
    const settings = { duration, voice_style: voiceStyle }
    
    try {
      setStatus('uploading')
      setError('')
      
      const response = await apiHelpers.uploadFile(file, settings)
      const { job_id } = response
      setJobId(job_id)
      setStatus('processing')
      
      // Start polling for status
      pollJobStatus(job_id)
      
    } catch (err: any) {
      setError(err.message || 'Có lỗi xảy ra khi upload')
      setStatus('error')
    }
  }

  const handleUploadUrl = async () => {
    if (!url.trim()) return
    
    const settings = { duration, voice_style: voiceStyle }
    
    try {
      setStatus('uploading')
      setError('')
      
      const response = await apiHelpers.processUrl(url, settings)
      const { job_id } = response
      setJobId(job_id)
      setStatus('processing')
      
      // Start polling for status
      pollJobStatus(job_id)
      
    } catch (err: any) {
      setError(err.message || 'Có lỗi xảy ra khi xử lý URL')
      setStatus('error')
    }
  }

  const pollJobStatus = async (jobId: string) => {
    try {
      const job = await apiHelpers.getJobStatus(jobId)
      
      setProgress(job.progress)
      setMessage(job.current_step || 'Đang xử lý...')
      
      if (job.status === 'completed') {
        setStatus('completed')
        setResult(job.result || null)
      } else if (job.status === 'failed') {
        setStatus('error')
        setError(job.error || 'Có lỗi xảy ra')
      } else {
        // Continue polling
        setTimeout(() => pollJobStatus(jobId), 2000)
      }
    } catch (err) {
      console.error('Error polling job status:', err)
      setTimeout(() => pollJobStatus(jobId), 5000) // Retry after 5s
    }
  }

  const handleDownload = async () => {
    if (!jobId) return
    
    try {
      const response = await apiHelpers.downloadFile(jobId)
      
      if (response.download_url) {
        const link = document.createElement('a')
        link.href = response.download_url
        link.setAttribute('download', `video_${jobId}.mp4`)
        document.body.appendChild(link)
        link.click()
        link.remove()
      }
    } catch (err) {
      console.error('Error downloading video:', err)
      setError('Không thể tải xuống video')
    }
  }

  const resetForm = () => {
    setStatus('idle')
    setJobId('')
    setProgress(0)
    setMessage('')
    setResult(null)
    setError('')
    setUrl('')
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: handleUploadFile,
    accept: {
      'application/pdf': ['.pdf'],
      'text/plain': ['.txt']
    },
    maxFiles: 1,
    maxSize: 50000000, // 50MB
  })

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold gradient-text mb-4">
            🎬 EBook to Video AI Generator
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Tạo video ngắn TikTok từ ebook/PDF tự động bằng AI. 
            Phân tích nội dung, tạo giọng đọc và video chuyên nghiệp trong vài phút.
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl p-8 animate-fade-in">
          
          {/* Input Type Toggle */}
          <div className="flex mb-8 p-1 bg-slate-100 dark:bg-slate-700 rounded-lg">
            <button
              type="button"
              onClick={() => setInputType('file')}
              className={`flex-1 py-3 px-4 rounded-md font-medium transition-all ${
                inputType === 'file'
                  ? 'bg-white dark:bg-slate-600 text-primary shadow-sm'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <FileText className="w-4 h-4 inline mr-2" />
              Upload PDF/TXT
            </button>
            <button
              type="button"
              onClick={() => setInputType('url')}
              className={`flex-1 py-3 px-4 rounded-md font-medium transition-all ${
                inputType === 'url'
                  ? 'bg-white dark:bg-slate-600 text-primary shadow-sm'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              <Globe className="w-4 h-4 inline mr-2" />
              Nhập URL
            </button>
          </div>

          {/* File Upload */}
          {inputType === 'file' && (
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all ${
                isDragActive
                  ? 'border-primary bg-primary/5'
                  : 'border-slate-300 dark:border-slate-600 hover:border-primary'
              }`}
            >
              <input {...getInputProps()} />
              <Upload className="w-12 h-12 mx-auto mb-4 text-slate-400" />
              {isDragActive ? (
                <p className="text-lg text-primary">Thả file vào đây...</p>
              ) : (
                <div>
                  <p className="text-lg text-foreground mb-2">
                    Kéo thả file hoặc click để chọn
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Hỗ trợ PDF, TXT (tối đa 50MB)
                  </p>
                </div>
              )}
            </div>
          )}

          {/* URL Input */}
          {inputType === 'url' && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">
                  URL bài viết hoặc ebook online
                </label>
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com/article"
                  className="w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white dark:bg-slate-700"
                />
              </div>
            </div>
          )}

          {/* Settings */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">
                <Settings className="w-4 h-4 inline mr-1" />
                Thời lượng video (giây)
              </label>
              <select
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value))}
                className="w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white dark:bg-slate-700"
              >
                <option value={60}>1 phút</option>
                <option value={120}>2 phút</option>
                <option value={180}>3 phút</option>
                <option value={300}>5 phút</option>
                <option value={600}>10 phút</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Phong cách giọng đọc
              </label>
              <select
                value={voiceStyle}
                onChange={(e) => setVoiceStyle(e.target.value)}
                className="w-full px-4 py-3 border border-slate-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white dark:bg-slate-700"
              >
                <option value="professional">Chuyên nghiệp</option>
                <option value="friendly">Thân thiện</option>
                <option value="authoritative">Uy quyền</option>
                <option value="inspiring">Truyền cảm hứng</option>
                <option value="educational">Giáo dục</option>
              </select>
            </div>
          </div>

          {/* Action Button */}
          <div className="mt-8">
            {status === 'idle' && (
              <button
                type="button"
                onClick={inputType === 'file' ? undefined : handleUploadUrl}
                disabled={inputType === 'url' && !url.trim()}
                className="w-full py-4 px-6 bg-primary text-primary-foreground rounded-lg font-semibold text-lg hover:bg-primary/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Play className="w-5 h-5 inline mr-2" />
                Tạo Video với AI
              </button>
            )}
          </div>

          {/* Progress */}
          {(status === 'uploading' || status === 'processing') && (
            <div className="mt-8 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Tiến độ</span>
                <span className="text-sm text-muted-foreground">{progress}%</span>
              </div>
              <div className="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-3">
                <div
                  className="bg-primary h-3 rounded-full transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <p className="text-center text-muted-foreground animate-pulse-slow">
                {message}
              </p>
            </div>
          )}

          {/* Error */}
          {status === 'error' && (
            <div className="mt-8 p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-destructive mr-2" />
                <span className="text-destructive font-medium">Lỗi:</span>
              </div>
              <p className="text-destructive mt-1">{error}</p>
              <button
                type="button"
                onClick={resetForm}
                className="mt-3 px-4 py-2 bg-destructive text-destructive-foreground rounded-lg text-sm hover:bg-destructive/90 transition-colors"
              >
                Thử lại
              </button>
            </div>
          )}

          {/* Results */}
          {status === 'completed' && result && (
            <div className="mt-8 space-y-6">
              <div className="flex items-center text-green-600 dark:text-green-400">
                <CheckCircle className="w-6 h-6 mr-2" />
                <span className="text-lg font-semibold">Video đã được tạo thành công!</span>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Video Download */}
                <div className="p-6 bg-slate-50 dark:bg-slate-700 rounded-xl">
                  <h3 className="font-semibold mb-4">📹 Video</h3>
                  <button
                    type="button"
                    onClick={handleDownload}
                    className="w-full py-3 px-4 bg-primary text-primary-foreground rounded-lg font-medium hover:bg-primary/90 transition-colors"
                  >
                    <Download className="w-4 h-4 inline mr-2" />
                    Tải xuống MP4
                  </button>
                </div>

                {/* Marketing Content */}
                <div className="p-6 bg-slate-50 dark:bg-slate-700 rounded-xl">
                  <h3 className="font-semibold mb-4">📱 Content Marketing</h3>
                  <div className="space-y-3 text-sm">
                    <div>
                      <strong>Caption:</strong>
                      <p className="text-muted-foreground mt-1">{result.marketing.caption}</p>
                    </div>
                    <div>
                      <strong>Hashtags:</strong>
                      <p className="text-blue-600 dark:text-blue-400 mt-1">
                        {result.marketing.hashtags.join(' ')}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Script Preview */}
              <div className="p-6 bg-slate-50 dark:bg-slate-700 rounded-xl">
                <h3 className="font-semibold mb-4">📝 Script</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {result.script}
                </p>
              </div>

              <button
                type="button"
                onClick={resetForm}
                className="w-full py-3 px-4 border border-slate-300 dark:border-slate-600 text-foreground rounded-lg font-medium hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
              >
                Tạo video mới
              </button>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-muted-foreground">
          <p>
            Powered by <span className="font-semibold">OpenAI GPT-4</span> + <span className="font-semibold">ElevenLabs</span>
          </p>
        </div>
      </div>
    </div>
  )
} 