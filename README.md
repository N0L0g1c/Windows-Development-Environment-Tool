# Windows Dev Environment Setup

Sets up your Windows dev environment without the usual headaches. Installs the tools you actually need and configures everything so you can start coding instead of fighting with setup.

## What it does

- **Gets the basics**: Git, Node.js, Python, VS Code/Cursor, Docker - all the usual suspects
- **Package managers**: Installs Chocolatey, Scoop, or Winget (your choice)
- **Development tools**: PowerShell modules, WSL, Windows Terminal, etc.
- **Actually works**: No more hunting down installers or dealing with PATH issues

*It's got some fancy stuff like automatic PATH configuration and dependency checking, but the basic setup works great without any configuration*

## Just run it

### GUI Version (Recommended)
```powershell
# Download and run the visual version
python dev-setup-gui.py

# Or use the launcher
python run-gui.py
```

**New GUI Features:**
- **Visual Setup**: Beautiful interface for selecting development stacks
- **Package Manager Detection**: Automatically detects and configures package managers
- **Real-time Progress**: Live installation progress with detailed logging
- **Stack Selection**: Easy selection of web dev, data science, .NET, mobile, and DevOps stacks
- **Custom Configuration**: Advanced settings for power users
- **Installation Log**: Real-time installation logs and error reporting

### PowerShell Version
```powershell
# Download and run (easiest way)
iwr -useb https://raw.githubusercontent.com/your-username/windows-dev-setup/main/setup.ps1 | iex

# Or download first, then run
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/your-username/windows-dev-setup/main/setup.ps1" -OutFile "setup.ps1"
.\setup.ps1
```

## What you can install

### Web Development (`--web-dev`)
Node.js, npm, VS Code/Cursor, browsers, databases - basically everything for web dev

### Data Science (`--data-science`)
Python, Jupyter, NumPy, Pandas, R, databases - all the data science goodies

### .NET Development (`--dotnet`)
.NET SDK, Visual Studio, Entity Framework, ASP.NET tools - Microsoft stack essentials

### Mobile Development (`--mobile-dev`)
Android Studio, Flutter, React Native - mobile dev essentials

### DevOps (`--devops`)
Docker, Kubernetes, Terraform, Azure CLI - for when you're managing infrastructure

*There's also some advanced stuff like automatic environment variable setup and registry tweaks, but honestly, the basic stuff works great*

## Works with your setup

- **Windows 10/11**: Works on both (though 11 is better)
- **Package managers**: Chocolatey, Scoop, Winget - picks what you have or installs one
- **Admin rights**: Some stuff needs admin, but it'll ask nicely
- **Existing tools**: Won't break what you already have installed

## How to use it

### Just run it
The script will ask what you want and handle the rest

### Or be specific
```powershell
# Install web dev stuff without questions
.\setup.ps1 --web-dev --non-interactive

# Just install what you need
.\setup.ps1 --tools git,nodejs,python,docker --non-interactive
```

*There's also a bunch of other options like `--debug`, `--dry-run`, and `--choco` if you want to get fancy*

## What it installs

### Package Managers (pick one)
- **Chocolatey**: The classic Windows package manager
- **Scoop**: Lightweight, no admin required
- **Winget**: Microsoft's official package manager

### Development Tools
- **Git**: Obviously
- **Node.js**: Latest LTS version
- **Python**: Latest stable version
- **VS Code/Cursor**: With useful extensions (you can choose)
- **Windows Terminal**: Better than the default
- **PowerShell**: Latest version with modules

### Optional Stuff
- **WSL**: Linux subsystem if you want it
- **Docker Desktop**: For containerization
- **Postman**: API testing
- **DBeaver**: Database management
- **Fiddler**: Web debugging

*It's got some smart detection to avoid installing stuff you already have, and it'll configure PATH variables automatically*

## Configuration

### Custom package lists
Create a `packages.txt` file with your custom package list:

```
# Custom packages
git
nodejs
python
vscode
docker-desktop
```

Then run:
```powershell
.\setup.ps1 --custom packages.txt
```

### Environment variables
The script sets up common environment variables:
- `NODE_PATH` for Node.js
- `PYTHONPATH` for Python
- `GIT_EDITOR` for your preferred editor
- `PATH` additions for installed tools

*There's also some registry tweaks for better development experience, but those are optional*

## Troubleshooting

### Common issues

1. **Execution Policy**: PowerShell might block the script
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Admin Rights**: Some tools need admin privileges
   ```powershell
   # Run PowerShell as Administrator
   .\setup.ps1
   ```

3. **Antivirus**: Some antivirus software might block downloads
   - Add the script to exclusions
   - Or download manually and run locally

### Debug mode
Enable debug mode for detailed logging:
```powershell
.\setup.ps1 --debug
```

*The script logs everything to `%TEMP%\dev-setup.log` so you can see what went wrong*

## Examples

### Basic web development setup
```powershell
.\setup.ps1 --web-dev
```

### Data science setup
```powershell
.\setup.ps1 --data-science
```

### Custom setup
```powershell
.\setup.ps1 --tools git,nodejs,python,vscode --choco
```

### Dry run (see what would be installed)
```powershell
.\setup.ps1 --web-dev --dry-run
```

*There's also some cool stuff like automatic VS Code/Cursor extension installation and PowerShell profile setup if you're into that*

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test on multiple Windows versions
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- Create an issue for bug reports
- Start a discussion for feature requests
- Check the wiki for additional documentation