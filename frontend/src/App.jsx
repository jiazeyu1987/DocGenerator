import React, { useEffect, useState, useRef } from "react";
import "./App.css";

const API_BASE = "";

function App() {
  const [file, setFile] = useState(null);
  const [markdownPreview, setMarkdownPreview] = useState("");
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [status, setStatus] = useState("");
  const [isConverting, setIsConverting] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef(null);

  useEffect(() => {
    // 检查后端健康状态
    fetch(`${API_BASE}/api/health`)
      .then((res) => res.json())
      .then((data) => {
        if (!data.pandoc_available) {
          setStatus("警告: Pandoc 不可用，转换功能可能无法使用");
        }
      })
      .catch(() => {
        setStatus("无法连接到后端服务");
      });

    // 获取模板列表
    fetch(`${API_BASE}/api/templates`)
      .then((res) => res.json())
      .then((data) => setTemplates(data))
      .catch(() => {
        setTemplates([]);
        setStatus(prev => prev ? prev : "无法获取模板列表");
      });
  }, []);

  const validateFile = (file) => {
    const validTypes = ['.md', '.markdown', 'text/markdown', 'text/plain'];
    const validExtensions = ['.md', '.markdown'];

    // 检查文件类型
    if (file && !validTypes.some(type => file.type.includes(type)) &&
        !validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))) {
      return false;
    }
    return true;
  };

  const processFile = (file) => {
    if (!validateFile(file)) {
      setStatus("请选择有效的 Markdown 文件 (.md, .markdown)");
      return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      setStatus("文件大小不能超过 10MB");
      return;
    }

    setFile(file);
    setStatus("");

    const reader = new FileReader();
    reader.onload = (e) => {
      setMarkdownPreview(e.target.result ?? "");
    };
    reader.onerror = () => {
      setStatus("读取文件失败");
    };
    reader.readAsText(file);
  };

  const handleFileChange = (event) => {
    const selected = event.target.files?.[0];
    if (!selected) {
      setFile(null);
      setMarkdownPreview("");
      return;
    }
    processFile(selected);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      processFile(files[0]);
    }
  };

  const openFileDialog = () => {
    fileInputRef.current?.click();
  };

  const handleTemplateChange = (event) => {
    setSelectedTemplate(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!file) {
      setStatus("请先选择一个 Markdown 文件");
      return;
    }

    setIsConverting(true);
    setStatus("正在转换，请稍候...");

    const formData = new FormData();
    formData.append("file", file);
    if (selectedTemplate) {
      formData.append("template", selectedTemplate);
    }

    try {
      const response = await fetch(`${API_BASE}/api/convert`, {
        method: "POST",
        body: formData
      });

      if (!response.ok) {
        let errorMessage = `转换失败 (${response.status})`;
        try {
          const errorData = await response.json();
          errorMessage = `转换失败: ${errorData.error || response.statusText}`;
        } catch {
          const errorText = await response.text();
          errorMessage = `转换失败: ${errorText || response.statusText}`;
        }
        setStatus(errorMessage);
        return;
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "document.docx";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      setStatus("✅ 转换完成，已开始下载");
    } catch (err) {
      console.error("Conversion error:", err);
      setStatus("❌ 转换时发生错误，请检查后端服务是否运行");
    } finally {
      setIsConverting(false);
    }
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>📝 Markdown 转 DOCX 工具</h1>
        <p className="subtitle">将您的 Markdown 文档转换为专业的 Word 文档</p>
      </div>

      <div className="main-content">
        <div className="upload-section">
          <div
            className={`upload-area ${isDragging ? 'dragging' : ''} ${file ? 'has-file' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={openFileDialog}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".md,.markdown,text/markdown,text/plain"
              onChange={handleFileChange}
              style={{ display: 'none' }}
            />

            {file ? (
              <div className="file-info">
                <div className="file-icon">📄</div>
                <div className="file-details">
                  <div className="file-name">{file.name}</div>
                  <div className="file-size">{(file.size / 1024).toFixed(1)} KB</div>
                </div>
                <button
                  type="button"
                  className="remove-file"
                  onClick={(e) => {
                    e.stopPropagation();
                    setFile(null);
                    setMarkdownPreview("");
                  }}
                >
                  ✕
                </button>
              </div>
            ) : (
              <div className="upload-prompt">
                <div className="upload-icon">📁</div>
                <h3>拖拽 Markdown 文件到此处</h3>
                <p>或点击选择文件</p>
                <small>支持 .md, .markdown 格式，最大 10MB</small>
              </div>
            )}
          </div>
        </div>

        {file && (
          <>
            <div className="template-section">
              <label htmlFor="template-select" className="template-label">
                选择 DOCX 模板（可选）：
              </label>
              <select
                id="template-select"
                value={selectedTemplate}
                onChange={handleTemplateChange}
                className="template-select"
                disabled={templates.length === 0}
              >
                <option value="">（不使用模板）</option>
                {templates.map((tpl) => (
                  <option key={tpl.name} value={tpl.name}>
                    {tpl.name}
                  </option>
                ))}
              </select>
              {templates.length === 0 && (
                <small className="no-templates">暂无可用模板</small>
              )}
            </div>

            <div className="action-section">
              <button
                type="button"
                onClick={handleSubmit}
                disabled={isConverting}
                className={`convert-button ${isConverting ? 'loading' : ''}`}
              >
                {isConverting ? (
                  <>
                    <span className="spinner"></span>
                    正在转换...
                  </>
                ) : (
                  <>
                    ⚡ 生成 DOCX
                  </>
                )}
              </button>
            </div>
          </>
        )}

        {status && (
          <div className={`status-message ${status.includes('✅') ? 'success' : status.includes('❌') || status.includes('警告') ? 'error' : 'info'}`}>
            {status}
          </div>
        )}

        {markdownPreview && (
          <div className="preview-section">
            <h2>📋 Markdown 预览</h2>
            <div className="preview-container">
              <textarea
                value={markdownPreview}
                readOnly
                className="preview-textarea"
                placeholder="Markdown 内容将在此处显示..."
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

