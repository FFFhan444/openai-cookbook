# Flask Portfolio Example

This folder contains a minimal portfolio website with a basic CMS built using Flask.

## Features

- Public pages:
  - **Home** page listing visible projects
  - **About** page with contact information
  - **Project detail** page for each project
- Admin pages:
  - Hard-coded login (`admin`/`password`)
  - Dashboard with list of all projects
  - Create, edit, and delete project entries
  - Toggle visibility of projects
- Project data stored in a simple JSON file

## Running locally

1. Install dependencies:
   ```bash
   pip install flask
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Visit `http://127.0.0.1:5000` in your browser.

## Deployment

This example can be deployed on services like [Render](https://render.com) using a free tier web service. Point the service to `python app.py` for the start command.
