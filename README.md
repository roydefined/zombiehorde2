
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
You have two options to pack and build Zombie Horde 2:

1. **Using PubDoomer (recommended)**  
   - Easiest option: all packing, compiling, and management happens inside PubDoomer.  
   - Requires:
     - [Clone PubDoomer](https://github.com/RoyDefined/PubDoomer) or use a prebuilt executable.
     - [.NET SDK 9.0.x](https://dotnet.microsoft.com/) (confirm with `dotnet --info`)  
     - (Optional) Visual Studio 2022 / Rider / VS Code.

2. **Without PubDoomer (manual build)**  
   - Use the provided `.bat` scripts:  
     - `pack-acsutils.bat` -> prepares ACSUtils into `dist/`  
     - `build-project.bat` -> compiles ACSUtils, library, and core ACS files  
   - No .NET or Visual Studio required.
   - Certain steps will take longer as no support is given.
   - Manual packing is **not** supported.

Additional tools you may want:
- Git with submodules support.
- [Zandronum 3.2.1](https://zandronum.com/download) or later (provided in `tools/`).
- For editing maps: [Ultimate Doom Builder](https://ultimatedoombuilder.github.io/) (provided in `tools/`).
- For editing maps and mod assets: [Slade 3](https://slade.mancubus.net/) (provided in `tools/`).

---

### 1) Fetch project
```bash
git clone --recurse-submodules https://github.com/RoyDefined/zombiehorde2
# Or if you already cloned the repo without `--recurse-submodules`:
# git submodule update --init --recursive
```

---

### 2) Build the project

#### Option A: Using PubDoomer
1. Run `pack-acsutils.bat`. This prepares ACSUtils into `modules\acsutils\dist`.  
2. Start PubDoomer.
3. Open `zh2project.pdtproj` in the application.
4. Go to the 'Profiles' tab.
5. Run the 'Compile project' profile.

#### Option B: Manually
1. Run `pack-acsutils.bat`. This prepares ACSUtils into `modules\acsutils\dist`.  
2. Run `build-project.bat`. This compiles all files.
   - `bcsutils.acs` -> `bcsutils.o`  
   - `zh2lib.acs` -> `zh2lib.o`  
   - `zh2game.acs` -> `zh2game.o` 

For both options, subsequent builds do not need another call of `pack-acsutils.bat`.

---

### 3) Edit / Run maps

#### Option A: Using PubDoomer
1. Start PubDoomer.
2. Open `zh2project.pdtproj`.
3. Go to the 'Maps & Archives' tab.
4. Pick one of the maps and open it in Zandronum, Ultimate Doom Builder, or Slade 3.

#### Option B: Manually
- You can find a build of Zandronum, Ultimate Doom Builder, or Slade 3 inside `tools/`.

In Ultimate Doom Builder, always use the `Zandronum_DoomUDMF` configuration as maps use UDMF format.

---

### 4) Pack project

#### With PubDoomer
1. Start PubDoomer.
2. Open `zh2project.pdtproj`.
3. Open the 'Profiles' tab.
4. Run one of the the 'Pack project' profiles depending on the desired result.
5. When finished you can press the 'Open working directory' button to open the project copy containing the build.
6. The build will be available in the root of the project.


#### Manual packing
Manual packing is currently not supported. If you intend to pack the mod, please use PubDoomer and pick one of the available profile options available.

---

> Having trouble? Join the [Discord server](https://Discord.RoyDefined.com/) for questions and support.
