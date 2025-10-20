#!/usr/bin/env python3
"""
Script de inicio simple para el microservicio ML
"""

import os
import sys
from app import create_app

def main():
    print("🚀 Iniciando microservicio ML...")
    print("📍 Puerto: 5001")
    print("🌐 URL: http://localhost:5001")
    print("-" * 40)
    
    try:
        app = create_app()
        app.run(host='0.0.0.0', port=5001, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Microservicio detenido")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

