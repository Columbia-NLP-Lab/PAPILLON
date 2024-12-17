# PAPILLON UI



## Features
- **Dynamic Prompt Generation**: Generate initial prompts based on user queries.
- **Prompt Editing and Tracking**: Record user edits with metadata like timestamps and length differences.
- **LLM Integration (Placeholder)**: Simulate calls to a cloud-based LLM.
- **HTML Interface**: Serve a basic user interface for interaction.

---

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

### Steps to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Create a Virtual Environment (Optional but Recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   Create a `requirements.txt` file with the following content:
   ```text
   fastapi
   uvicorn
   pydantic
   jinja2
   ```
   Then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Directory Structure**:
   Ensure your project directory has the following structure:
   ```
   .
   |-- app.py                 # Main application file
   |-- requirements.txt       # List of dependencies
   |-- static/                # Directory for static files (CSS/JS/images)
   |-- templates/             # Directory for HTML templates
       |-- index.html         # Main template file
   ```

5. **Run the Application**:
   Start the server using:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8012
   ```
   The application will be accessible at `http://127.0.0.1:8012/`.

---

## API Endpoints

### 1. Root Endpoint (`/`)
- **Type**: GET
- **Description**: Serves the main HTML interface (`index.html`).

### 2. Generate Prompt (`/generate_prompt`)
- **Type**: POST
- **Input**:
  ```json
  {
      "query": "<user_query_string>"
  }
  ```
- **Response**:
  ```json
  {
      "prompt": "<generated_prompt_string>"
  }
  ```

### 3. Process Prompt (`/process_prompt`)
- **Type**: POST
- **Input**:
  ```json
  {
      "original_prompt": "<original_prompt_string>",
      "edited_prompt": "<edited_prompt_string>"
  }
  ```
- **Response**:
  ```json
  {
      "output": "<final_output_string>",
      "edit_record": {
          "timestamp": "<ISO_timestamp>",
          "original": "<original_prompt_string>",
          "edited": "<edited_prompt_string>",
          "diff_length": <length_difference>
      }
  }
  ```

---

## Directory and File Overview

- **`app.py`**: Main application logic, including API endpoints and pipeline handling.
- **`requirements.txt`**: Dependencies for running the application.
- **`static/`**: Directory for static assets (e.g., CSS, JS files, images).
- **`templates/`**: Directory for Jinja2 HTML templates.
  - `index.html`: Main HTML page served at the root endpoint.

---



## Troubleshooting

1. **Dependency Issues**:
   Ensure all dependencies in `requirements.txt` are installed. Use:
   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**:
   If port 8012 is busy, run the server on a different port:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port <new_port>
   ```

3. **Template Errors**:
   Ensure the `templates/` directory exists and contains `index.html`.

---

Feel free to reach out for further questions or enhancements!


