import os
from app import app

if 'PORT' in os.environ:
    app.run(debug=False, host='0.0.0.0', port=os.environ['PORT'])
else:
    app.run(debug=True, host='0.0.0.0', port=80)
