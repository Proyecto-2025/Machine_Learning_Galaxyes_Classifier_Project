#!/usr/bin/env python3
"""
Script de inicio para el microservicio ML
Permite iniciar el servidor con configuración personalizada
"""

import argparse
import os
import sys
from app import create_app

def main():
    parser = argparse.ArgumentParser(description='Iniciar el microservicio ML')
    parser.add_argument('--host', default='0.0.0.0', help='Host del servidor (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5001, help='Puerto del servidor (default: 5001)')
    parser.add_argument('--debug', action='store_true', help='Activar modo debug')
    parser.add_argument('--backend-url', default='http://localhost:5000', 
                       help='URL del backend principal (default: http://localhost:5000)')
    
    args = parser.parse_args()
    
    # Establecer variables de entorno
    os.environ['HOST'] = args.host
    os.environ['PORT'] = str(args.port)
    os.environ['DEBUG'] = str(args.debug).lower()
    os.environ['BACKEND_URL'] = args.backend_url
    
    print(f"🚀 Iniciando microservicio ML...")
    print(f"📍 Host: {args.host}")
    print(f"🔌 Puerto: {args.port}")
    print(f"🐛 Debug: {args.debug}")
    print(f"🔗 Backend URL: {args.backend_url}")
    print(f"🌐 URL completa: http://{args.host}:{args.port}")
    print("-" * 50)
    
    try:
        app = create_app()
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n👋 Microservicio detenido por el usuario")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error al iniciar el microservicio: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

