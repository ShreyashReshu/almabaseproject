# Deployment Guide

This Django REST API can be deployed to various platforms. Here are the recommended options:

## Option 1: Railway (Recommended - Easiest)

1. Push your code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Sign up with GitHub
4. Click "New Project" → "Deploy from GitHub repo"
5. Select your repository
6. Railway will auto-detect the Django app
7. Add environment variables if needed
8. Your app will be live!

**Note:** Update `ALLOWED_HOSTS` in `app/app/settings.py` with your Railway URL after deployment.

## Option 2: Render

1. Push code to GitHub
2. Go to [Render.com](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Settings:
   - **Build Command:** `cd app && pip install -r requirements.txt && python manage.py migrate`
   - **Start Command:** `cd app && gunicorn app.wsgi:application --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3
6. Deploy!

## Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set buildpacks: `heroku buildpacks:set heroku/python`
5. Deploy: `git push heroku main`
6. Run migrations: `heroku run python app/manage.py migrate`

## Option 4: PythonAnywhere

1. Create free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code via Git
3. Configure a web app
4. Set working directory to your Django project
5. Update WSGI configuration file
6. Reload web app

## Local Development

```bash
# Navigate to the app folder
cd app

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Access the app at: `http://localhost:8000/`

## Environment Variables

For production, set these environment variables:

- `DEBUG=False` (disable debug mode)
- `SECRET_KEY` (generate a new secret key for production)
- `ALLOWED_HOSTS` (your domain name)

## Database

The app currently uses SQLite for development. For production, consider:

1. **PostgreSQL** (recommended for production)
2. **MySQL**
3. **Cloud databases** (AWS RDS, Railway Postgres, etc.)

Update `DATABASES` in `app/app/settings.py` for production databases.

## Static Files

For production, configure static files collection:

```python
# In settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

Then run:
```bash
python manage.py collectstatic
```

## Testing the API

Once deployed, test the endpoints:

```bash
# Example: Get access token
curl -X POST https://your-app-url.com/api/user/login \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "password": "test123"}'
```

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [DRF Documentation](https://www.django-rest-framework.org/)
- [Gunicorn Documentation](https://gunicorn.org/)

