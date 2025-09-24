
<div align="center">
	<img src="https://github.com/RoyDefined/zombiehorde2/blob/main/docs/logo.png?raw=true" />
</div>

<div align="center">
	<h5>Zombie Horde 2 is a multiplayer mod for Zandronum and the sequel to Zombie Horde by Xsnake.</h5>
	<a href="https://Discord.RoyDefined.com/"><img src="https://img.shields.io/discord/1154064438551400538?style=flat&label=Join%20Community&color=7289DA" /></a>
	<a href="https://www.RoyDefined.com/"><img src="https://img.shields.io/badge/RoyDefined.com-blue" /></a>
</div>

> [!WARNING]  
> **Zombie Horde 2 is currently in a beta state**. Content is subject to change, and you may encounter bugs.

## Setup

### Prerequisites
- **PubDoomer** is used to build and pack the project.
	- .NET SDK **9.0.x** (confirm with `dotnet --info`)
	- (Optional) Visual Studio 2022 / Rider / VS Code
	- [Clone the project.](https://github.com/RoyDefined/PubDoomer)
- Git with submodules support.
- [Zandronum 3.2.1](https://zandronum.com/download) or later.
- For opening and editing maps, [Ultimate Doom Builder](https://ultimatedoombuilder.github.io/).
- For opening and editing maps and the mod itself, [Slade 3](https://slade.mancubus.net/).

### 1) Fetch project
#### 1.1 Clone project
1. Run a clone of the project in the command line.
```bash
git clone --recurse-submodules https://github.com/RoyDefined/zombiehorde2
# Or if you already cloned the repo without `--recurse-submodules`:
# git submodule update --init --recursive
```

#### 1.2 Set up ACSUtils (manual compilation)
1. Navigate to `Path/To/zombiehorde2/modules/acsutils`.
2. Create a `.bat` file with the following content:
	```bash
	call tools\build.bat
	```
3. Run the `.bat` file.
	- Note the process wil succeed to provide a '/dist' folder but fail to compile the project.
	- Actual compilation is done by PubDoomer, and as such this step is not required to complete.

#### 1.2 Set up ACSUtils (does not require manual compilation)
1. [Download](https://github.com/Korshun/acsutils/releases) the latest release of ACSUtils.
2. Navigate to `Path/To/zombiehorde2/modules/acsutils`.
3. Create a folder '/dist'.
4. Move the contents of the downloaded zipfile in the '/dist' folder.

### 2) Build
1. Start up PubDoomer.
2. Open `zh2project.pdtproj` in the application.
3. Open the 'Profiles' tab.
4. Run the 'Compile project' profile.

### 3) Edit / Run maps
1. Start up PubDoomer.
2. Open `zh2project.pdtproj` in the application.
3. Open the 'Maps & Archives' tab.
4. Pick one of the maps, and using one of the three buttons either open the map in Zandronum, Ultimate Doom Builder or Slade 3.
	- Note opening the map in Doom Builder asks for one of many configurations. Unless otherwise specified, you must pick 'Zandronum_DoomUDMF'.

### 4) Pack project
1. Start up PubDoomer.
2. Open `zh2project.pdtproj` in the application.
3. Open the 'Profiles' tab.
4. Run the 'Pack project' profile.
5. When finished you can press the 'Open working directory' button to open the project copy containing the build.
6. The build will be available in the root of the project.

> Having trouble? The Discord server is the best location for questions and help.
