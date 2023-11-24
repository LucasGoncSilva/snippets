# Vercel

```json title="vercel.json"
{
  "builds": [
    {
      "src": "LIPSUM/wsgi.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "300mb",
        "runtime": "python3.9"
      }
    },
    {
      // "src": "deploy.sh",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "staticfiles"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "LIPSUM/wsgi.py"
    }
  ]
}
```
