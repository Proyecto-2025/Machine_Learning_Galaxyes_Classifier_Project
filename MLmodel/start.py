#!/usr/bin/env python3
"""
Script de inicio simple para el microservicio ML
"""

import os
import sys
from app import create_app

def main():
    # Leer puerto de variable de entorno (Cloud Run usa PORT=8080)
    port = int(os.environ.get('PORT', 5001))

    print("🚀 Iniciando microservicio ML...")
    print(f"📍 Puerto: {port}")
    print(f"🌐 URL: http://0.0.0.0:{port}")
    print("-" * 40)
    
    try:
        app = create_app()
        app.run(host='0.0.0.0', port=port, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Microservicio detenido")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

