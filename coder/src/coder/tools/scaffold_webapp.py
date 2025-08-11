from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field, validator


class ScaffoldBaseInput(BaseModel):
    project_name: str = Field(..., description="Name of the project directory to create under output/")
    typescript: bool = Field(True, description="Whether to scaffold a TypeScript project")
    tailwind: bool = Field(True, description="Whether to configure Tailwind CSS")
    package_manager: Literal["npm", "yarn", "pnpm"] = Field(
        "npm", description="Preferred package manager for scripts in package.json"
    )
    target_root: str = Field(
        "output", description="Root folder where the project folder will be created"
    )

    @validator("project_name")
    def validate_project_name(cls, value: str) -> str:
        if not value or any(ch in value for ch in "\t\n\r/\\:"):
            raise ValueError("Invalid project_name. Use a simple folder name without path separators.")
        return value


class NextJsScaffoldInput(ScaffoldBaseInput):
    app_router: bool = Field(True, description="Use Next.js App Router structure")


class ReactViteScaffoldInput(ScaffoldBaseInput):
    pass


class _ScaffoldUtils:
    @staticmethod
    def ensure_dir(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def write_file(path: Path, content: str) -> None:
        _ScaffoldUtils.ensure_dir(path.parent)
        path.write_text(content, encoding="utf-8")

    @staticmethod
    def format_package_json_scripts(pm: str, scripts: dict[str, str]) -> str:
        import json

        return (
            json.dumps(
                {
                    "name": "app",
                    "version": "0.1.0",
                    "private": True,
                    "type": "module",
                    "scripts": scripts,
                },
                indent=2,
            )
            + "\n"
        )


class NextJsScaffoldTool(BaseTool):
    name: str = "NextJsScaffoldTool"
    description: str = (
        "Scaffolds a minimal Next.js project under output/<project_name> with optional TypeScript and Tailwind. "
        "Generates common files (package.json, next.config.js, tsconfig if TS, app/pages, styles, Tailwind config). "
        "It does not run npm install; it writes project files ready for you to install."
    )
    args_schema: Type[BaseModel] = NextJsScaffoldInput

    def _run(
        self,
        project_name: str,
        typescript: bool = True,
        tailwind: bool = True,
        package_manager: str = "npm",
        target_root: str = "output",
        app_router: bool = True,
    ) -> str:
        base_path = Path(target_root) / project_name
        _ScaffoldUtils.ensure_dir(base_path)

        # package.json
        scripts = {
            "dev": "next dev",
            "build": "next build",
            "start": "next start",
            "lint": "next lint",
        }
        if tailwind:
            scripts["format"] = (
                "prettier --write ." if package_manager else "prettier --write ."
            )
        _ScaffoldUtils.write_file(
            base_path / "package.json",
            _ScaffoldUtils.format_package_json_scripts(package_manager, scripts),
        )

        # next.config.js
        _ScaffoldUtils.write_file(
            base_path / "next.config.js",
            """/** @type {import('next').NextConfig} */\nconst nextConfig = { reactStrictMode: true };\nmodule.exports = nextConfig;\n""",
        )

        # tsconfig.json or jsconfig.json
        if typescript:
            _ScaffoldUtils.write_file(
                base_path / "tsconfig.json",
                """{\n  "compilerOptions": {\n    "target": "ES2020",\n    "lib": ["dom", "dom.iterable", "esnext"],\n    "allowJs": false,\n    "skipLibCheck": true,\n    "strict": true,\n    "noEmit": true,\n    "esModuleInterop": true,\n    "module": "esnext",\n    "moduleResolution": "bundler",\n    "resolveJsonModule": true,\n    "isolatedModules": true,\n    "jsx": "preserve",\n    "incremental": true,\n    "plugins": [{ "name": "next" }]\n  },\n  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],\n  "exclude": ["node_modules"]\n}\n""",
            )
            _ScaffoldUtils.write_file(
                base_path / "next-env.d.ts",
                """/// <reference types="next" />\n/// <reference types="next/image-types/global" />\n// NOTE: This file should not be edited\n""",
            )
        else:
            _ScaffoldUtils.write_file(
                base_path / "jsconfig.json",
                """{\n  "compilerOptions": {\n    "target": "ES2020",\n    "lib": ["dom", "dom.iterable", "esnext"],\n    "allowJs": true,\n    "skipLibCheck": true,\n    "strict": false,\n    "noEmit": true,\n    "module": "esnext",\n    "moduleResolution": "bundler",\n    "resolveJsonModule": true,\n    "isolatedModules": true,\n    "jsx": "preserve"\n  },\n  "include": ["**/*.js", "**/*.jsx"],\n  "exclude": ["node_modules"]\n}\n""",
            )

        # Directory structure
        if app_router:
            app_dir = base_path / "app"
            _ScaffoldUtils.ensure_dir(app_dir / "styles")
            page_ext = "tsx" if typescript else "jsx"
            _ScaffoldUtils.write_file(
                app_dir / f"page.{page_ext}",
                (
                    """export default function Home() {\n  return (\n    <main style={{ padding: 24 }}>\n      <h1>Next.js App Router</h1>\n      <p>Scaffolded project is ready.</p>\n    </main>\n  );\n}\n"""
                ),
            )
            styles_path = app_dir / "globals.css"
        else:
            pages_dir = base_path / "pages"
            _ScaffoldUtils.ensure_dir(pages_dir)
            page_ext = "tsx" if typescript else "jsx"
            _ScaffoldUtils.write_file(
                pages_dir / f"index.{page_ext}",
                """export default function Home() {\n  return (\n    <main style={{ padding: 24 }}>\n      <h1>Next.js Pages Router</h1>\n      <p>Scaffolded project is ready.</p>\n    </main>\n  );\n}\n""",
            )
            styles_path = base_path / "styles" / "globals.css"

        # Tailwind setup (files only)
        if tailwind:
            _ScaffoldUtils.write_file(
                base_path / "postcss.config.js",
                """module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };\n""",
            )
            _ScaffoldUtils.write_file(
                base_path / "tailwind.config.js",
                (
                    """/** @type {import('tailwindcss').Config} */\nmodule.exports = {\n  content: [\n    "./app/**/*.{js,ts,jsx,tsx}",\n    "./pages/**/*.{js,ts,jsx,tsx}",\n    "./components/**/*.{js,ts,jsx,tsx}",\n  ],\n  theme: { extend: {} },\n  plugins: [],\n};\n"""
                ),
            )
            _ScaffoldUtils.write_file(
                styles_path,
                """@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\nbody {\n  @apply antialiased;\n}\n""",
            )
        else:
            _ScaffoldUtils.write_file(
                styles_path,
                """* { box-sizing: border-box; }\nbody { margin: 0; font-family: ui-sans-serif, system-ui, -apple-system; }\n""",
            )

        # Minimal README
        _ScaffoldUtils.write_file(
            base_path / "README_GEN.md",
            f"""# {project_name}\n\nThis project was scaffolded by NextJsScaffoldTool.\n\n## Getting Started\n\n1. Install dependencies:\n\n   {package_manager} install\n\n2. Run the development server:\n\n   {package_manager} run dev\n\n## Notes\n- Tailwind: {'enabled' if tailwind else 'disabled'}\n- TypeScript: {'enabled' if typescript else 'disabled'}\n- Router: {'App Router' if app_router else 'Pages Router'}\n""",
        )

        return str(base_path)


class ReactViteScaffoldTool(BaseTool):
    name: str = "ReactViteScaffoldTool"
    description: str = (
        "Scaffolds a minimal React + Vite project under output/<project_name> with optional TypeScript and Tailwind. "
        "Generates common files (package.json, vite config, tsconfig/jsconfig, index.html, src files, Tailwind config). "
        "It does not run npm install; it writes project files ready for you to install."
    )
    args_schema: Type[BaseModel] = ReactViteScaffoldInput

    def _run(
        self,
        project_name: str,
        typescript: bool = True,
        tailwind: bool = True,
        package_manager: str = "npm",
        target_root: str = "output",
    ) -> str:
        base_path = Path(target_root) / project_name
        _ScaffoldUtils.ensure_dir(base_path)

        # package.json
        scripts = {
            "dev": "vite",
            "build": "tsc -b && vite build" if typescript else "vite build",
            "preview": "vite preview",
        }
        _ScaffoldUtils.write_file(
            base_path / "package.json",
            _ScaffoldUtils.format_package_json_scripts(package_manager, scripts),
        )

        # Vite config
        if typescript:
            _ScaffoldUtils.write_file(
                base_path / "vite.config.ts",
                """import { defineConfig } from 'vite'\nimport react from '@vitejs/plugin-react'\n\nexport default defineConfig({ plugins: [react()] })\n""",
            )
            _ScaffoldUtils.write_file(
                base_path / "tsconfig.json",
                """{\n  "compilerOptions": {\n    "target": "ES2020",\n    "useDefineForClassFields": true,\n    "lib": ["ES2020", "DOM", "DOM.Iterable"],\n    "module": "ESNext",\n    "skipLibCheck": true,\n    "jsx": "react-jsx",\n    "moduleResolution": "Bundler",\n    "resolveJsonModule": true,\n    "isolatedModules": true,\n    "noEmit": true,\n    "strict": true\n  },\n  "include": ["src"]\n}\n""",
            )
        else:
            _ScaffoldUtils.write_file(
                base_path / "vite.config.js",
                """import { defineConfig } from 'vite'\nimport react from '@vitejs/plugin-react'\n\nexport default defineConfig({ plugins: [react()] })\n""",
            )

        # index.html
        _ScaffoldUtils.write_file(
            base_path / "index.html",
            """<!doctype html>\n<html lang="en">\n  <head>\n    <meta charset="UTF-8" />\n    <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n    <title>React + Vite</title>\n  </head>\n  <body>\n    <div id="root"></div>\n    <script type="module" src="/src/main."""
            + ("tsx" if typescript else "jsx")
            + "\"></script>\n  </body>\n</html>\n",
        )

        # src files
        src_dir = base_path / "src"
        _ScaffoldUtils.ensure_dir(src_dir)
        ext = "tsx" if typescript else "jsx"
        _ScaffoldUtils.write_file(
            src_dir / f"main.{ext}",
            (
                """import React from 'react'\nimport ReactDOM from 'react-dom/client'\nimport App from './App'\nimport './index.css'\n\nReactDOM.createRoot(document.getElementById('root')!).render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>,\n)\n"""
                if typescript
                else
                """import React from 'react'\nimport ReactDOM from 'react-dom/client'\nimport App from './App'\nimport './index.css'\n\nReactDOM.createRoot(document.getElementById('root')).render(\n  <React.StrictMode>\n    <App />\n  </React.StrictMode>,\n)\n"""
            ),
        )
        _ScaffoldUtils.write_file(
            src_dir / f"App.{ext}",
            """export default function App() {\n  return (\n    <div style={{ padding: 24 }}>\n      <h1>React + Vite</h1>\n      <p>Scaffolded project is ready.</p>\n    </div>\n  )\n}\n""",
        )

        # styling
        if tailwind:
            _ScaffoldUtils.write_file(
                base_path / "postcss.config.js",
                """module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } };\n""",
            )
            _ScaffoldUtils.write_file(
                base_path / "tailwind.config.js",
                """/** @type {import('tailwindcss').Config} */\nmodule.exports = {\n  content: [\n    "./index.html",\n    "./src/**/*.{js,ts,jsx,tsx}",\n  ],\n  theme: { extend: {} },\n  plugins: [],\n};\n""",
            )
            _ScaffoldUtils.write_file(
                src_dir / "index.css",
                """@tailwind base;\n@tailwind components;\n@tailwind utilities;\n""",
            )
        else:
            _ScaffoldUtils.write_file(
                src_dir / "index.css",
                """* { box-sizing: border-box; }\nbody { margin: 0; font-family: ui-sans-serif, system-ui, -apple-system; }\n""",
            )

        # README
        _ScaffoldUtils.write_file(
            base_path / "README_GEN.md",
            f"""# {project_name}\n\nThis project was scaffolded by ReactViteScaffoldTool.\n\n## Getting Started\n\n1. Install dependencies:\n\n   {package_manager} install\n\n2. Run the development server:\n\n   {package_manager} run dev\n\n## Notes\n- Tailwind: {'enabled' if tailwind else 'disabled'}\n- TypeScript: {'enabled' if typescript else 'disabled'}\n""",
        )

        return str(base_path)


