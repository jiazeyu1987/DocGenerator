# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Markdown-to-DOCX conversion tool with a web interface. The application consists of:

- **Backend**: Flask-based Python API that handles file conversion using Pandoc
- **Frontend**: React web interface built with Vite for uploading and converting files
- **Special Feature**: Mermaid diagram processing that converts code blocks to images

## Development Commands

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev     # Development server on port 3000
npm run build   # Production build
npm run preview # Preview production build
```

### Template Management
```bash
cd backend
python create_templates.py    # Create DOCX templates
python create_blank_docx.py   # Create blank template
```

### Testing and Debugging
```bash
# Enable test mode for Mermaid processing (set environment variables)
export MERMAID_TEST_MODE=true
export MERMAID_TEST_OUTPUT_DIR=d:/tmp/mermaid_test
```

## Architecture Overview

### Backend Structure
- `app.py`: Main Flask application with API endpoints
- `mermaid_processor.py`: Mermaid diagram conversion module
- `create_templates.py`: Template creation utilities
- `templates_store/`: Directory for DOCX template files

### Frontend Structure
- `src/App.jsx`: Main React component with file upload and conversion
- `vite.config.js`: Vite configuration with API proxy to backend

### Key API Endpoints
- `GET /api/health`: Check backend health and Pandoc availability
- `GET /api/templates`: List available DOCX templates
- `POST /api/convert`: Convert Markdown to DOCX

## Dependencies and External Tools

### Python Dependencies
- Flask 2.3.3: Web framework
- Flask-CORS 4.0.0: Cross-origin resource sharing
- Pandoc: Required for document conversion (must be installed separately)
- Mermaid CLI (`@mermaid-js/mermaid-cli`): Required for diagram conversion

### Node.js Dependencies
- React 18.3.1: Frontend framework
- Vite 5.4.0: Build tool and dev server

### System Requirements
- Pandoc must be installed and available in PATH
- Mermaid CLI (`mmdc`) must be installed globally via npm
- Backend runs on port 5000, frontend on port 3000

## Development Workflow

1. **Setup**: Install Python/Node dependencies and external tools (Pandoc, Mermaid CLI)
2. **Backend**: Start Flask server on port 5000
3. **Frontend**: Start Vite dev server on port 3000 (includes proxy to backend)
4. **Templates**: Use `create_templates.py` to generate DOCX templates
5. **Testing**: Use environment variables for test mode debugging

## File Processing Flow

1. User uploads Markdown file via React frontend
2. Backend validates file (type, size, content)
3. MermaidProcessor extracts and converts Mermaid diagrams to PNG images
4. Pandoc converts processed Markdown to DOCX using selected template
5. Temporary files are cleaned up after conversion (delayed cleanup for download)

## Configuration

### Environment Variables
- `UPLOAD_FOLDER`: Temporary file upload directory
- `TEMPLATE_FOLDER`: DOCX templates directory
- `MERMAID_TEST_MODE`: Enable debug mode for Mermaid processing
- `MERMAID_TEST_OUTPUT_DIR`: Debug output directory for test mode

### Vite Proxy Configuration
Frontend development server proxies `/api/*` requests to `http://localhost:5000`

## Security Considerations

- File upload validation (type, size, filename safety)
- Path traversal protection for template files
- Temporary file cleanup with delayed deletion
- Content validation to prevent binary file uploads

## Common Issues and Solutions

1. **Pandoc not found**: Install Pandoc and ensure it's in PATH
2. **Mermaid conversion fails**: Install `@mermaid-js/mermaid-cli` globally
3. **Template not found**: Check `templates_store/` directory and file permissions
4. **CORS issues**: Backend includes Flask-CORS configuration