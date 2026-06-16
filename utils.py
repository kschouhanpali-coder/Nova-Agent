import os
import base64


def save_env_var(var_name, value):
    """Save or update an environment variable in the .env file."""
    env_path = ".env"
    if not os.path.exists(env_path):
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"{var_name}={value}\n")
        return
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    key_exists = False
    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{var_name}="):
            new_lines.append(f"{var_name}={value}\n")
            key_exists = True
        else:
            new_lines.append(line)
    if not key_exists:
        new_lines.append(f"\n{var_name}={value}\n")
    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def save_key_to_env(key):
    """Convenience wrapper to save Gemini API key."""
    save_env_var("GEMINI_API_KEY", key)


def get_svg_avatar_base64(color_hex):
    """Generate an animated 3D core SVG avatar as a base64 data URI."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" />
      <stop offset="40%" stop-color="{color_hex}" />
      <stop offset="100%" stop-color="transparent" />
    </radialGradient>
  </defs>
  <!-- Glowing background space -->
  <circle cx="50" cy="50" r="30" fill="url(#glow)" opacity="0.35" />
  
  <!-- Outer Spinning Dashed Ring -->
  <ellipse cx="50" cy="50" rx="42" ry="15" fill="none" stroke="{color_hex}" stroke-width="2" stroke-dasharray="6 6">
    <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="8s" repeatCount="indefinite" />
  </ellipse>
  
  <!-- Inner Orbiting Solid Ring 1 (Tilted X) -->
  <ellipse cx="50" cy="50" rx="36" ry="12" fill="none" stroke="{color_hex}" stroke-width="2.5" transform="rotate(45 50 50)">
    <animateTransform attributeName="transform" type="rotate" from="45 50 50" to="405 50 50" dur="5s" repeatCount="indefinite" />
  </ellipse>

  <!-- Inner Orbiting Solid Ring 2 (Tilted Z) -->
  <ellipse cx="50" cy="50" rx="36" ry="12" fill="none" stroke="{color_hex}" stroke-width="2.5" transform="rotate(-45 50 50)">
    <animateTransform attributeName="transform" type="rotate" from="-45 50 50" to="-405 50 50" dur="4s" repeatCount="indefinite" />
  </ellipse>
  
  <!-- Glowing central dot -->
  <circle cx="50" cy="50" r="14" fill="url(#glow)" opacity="0.8">
    <animate attributeName="r" values="10;15;10" dur="2s" repeatCount="indefinite" />
  </circle>
  <circle cx="50" cy="50" r="6" fill="#ffffff" />
</svg>"""
    encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"


def get_user_svg_avatar_base64():
    """Generate a user avatar SVG as a base64 data URI."""
    color = "#94a3b8"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <radialGradient id="userGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#64748b" />
      <stop offset="100%" stop-color="transparent" />
    </radialGradient>
  </defs>
  <circle cx="50" cy="50" r="45" fill="url(#userGlow)" opacity="0.25" />
  <circle cx="50" cy="50" r="40" fill="none" stroke="{color}" stroke-width="2" opacity="0.3" />
  <path d="M50 45c5.5 0 10-4.5 10-10s-4.5-10-10-10-10 4.5-10 10 4.5 10 10 10zm0 8c-9.3 0-28 4.7-28 14v6h56v-6c0-9.3-18.7-14-28-14z" fill="{color}" />
</svg>"""
    encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"
