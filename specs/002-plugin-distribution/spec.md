# Feature Specification: Plugin & Distribution Packaging

**Feature Branch**: `002-plugin-distribution`
**Created**: 2026-03-22
**Status**: Draft
**Input**: User description: "We also want to make sure we can deliver this as a plugin for claude like we do in mcp-outline. Not sure yet if we should add in a specialised skill or agent yet but we need to plan in the marketplace and plugin files. Should also be able to deliver it as a dxc file or what it is that claude desktop uses"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install via Claude Code Plugin (Priority: P1)

A Claude Code user discovers mcp-tekna in the plugin marketplace or via a direct link. They install it with a single command and immediately have access to Tekna event search, news, and member benefits tools within their Claude Code session. No manual configuration or environment variables are required since the server uses only public data.

**Why this priority**: Claude Code is the primary development environment where MCP servers are consumed. Plugin marketplace visibility drives adoption, and zero-config installation (no API keys needed) makes this an ideal first distribution channel.

**Independent Test**: Can be fully tested by installing the plugin from its repository URL and verifying that Tekna MCP tools appear and function in a Claude Code session.

**Acceptance Scenarios**:

1. **Given** the plugin files are correctly structured in the repository, **When** a user runs the plugin install command, **Then** the MCP server is registered and Tekna tools are available in their session.
2. **Given** a user has installed the plugin, **When** they start a new Claude Code session, **Then** the MCP server starts automatically and tools are listed.
3. **Given** the plugin is installed, **When** the user invokes a Tekna tool (e.g., search events), **Then** the tool executes and returns results from tekna.no.
4. **Given** the plugin manifest exists, **When** a marketplace crawler indexes the repository, **Then** the plugin appears with correct name, description, version, and keywords.

---

### User Story 2 - Install via Claude Desktop (Priority: P2)

A non-developer Tekna member wants to ask Claude about upcoming events or news. They install the mcp-tekna server into Claude Desktop either by adding it to their configuration file manually or by using a pre-built desktop extension package. Once installed, they can ask Claude questions about Tekna events, news, and benefits in natural language.

**Why this priority**: Claude Desktop is the primary consumer-facing client. Supporting it expands the audience beyond developers. The user wants a desktop extension file format for easy installation.

**Independent Test**: Can be fully tested by configuring Claude Desktop with the MCP server entry and verifying Tekna tools appear and respond to queries.

**Acceptance Scenarios**:

1. **Given** the MCP server registry file exists in the repository, **When** a user adds the server to their Claude Desktop config, **Then** the MCP server starts and Tekna tools are available.
2. **Given** the server is published to a package registry, **When** a user configures Claude Desktop to use it via the registry runner, **Then** the server starts without additional setup.
3. **Given** a desktop extension package is available, **When** a user installs it through Claude Desktop's extension mechanism, **Then** the server is automatically configured and tools are available.

---

### User Story 3 - Install via Docker or Remote URL (Priority: P3)

A user who prefers hosted or containerized deployments runs the mcp-tekna server as a Docker container or connects to a hosted instance via a remote URL. This supports claude.ai web users who add custom MCP connectors by URL, as well as teams who want a shared server instance.

**Why this priority**: Supports the project goal of a "public MCP server that people can connect to" and enables claude.ai web connector support. Lower priority because it requires hosting infrastructure.

**Independent Test**: Can be fully tested by running the Docker container and connecting to it via streamable-http from any MCP client.

**Acceptance Scenarios**:

1. **Given** a container build file exists in the repository, **When** a user builds and runs the container, **Then** the MCP server starts and accepts streamable-http connections.
2. **Given** the server is running as a hosted instance, **When** a claude.ai user adds the URL as a custom connector, **Then** Tekna tools appear and function in their web session.
3. **Given** the container image is published to a container registry, **When** a user pulls and runs it, **Then** the server starts with sensible defaults and no required configuration.

---

### Edge Cases

- What happens when a user installs the plugin but has no internet connection to reach tekna.no?
- How does the plugin handle version mismatches between the plugin manifest and the installed server version?
- What happens if a user already has a different MCP server named "mcp-tekna" configured?
- How does the system behave when Claude Desktop or Claude Code updates their plugin/extension format?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Repository MUST contain a Claude Code plugin manifest with name, description, version, author, homepage, repository, license, and keywords.
- **FR-002**: Repository MUST contain an MCP server registry manifest following the official MCP server schema, declaring the package registry, transport type, and runtime hint.
- **FR-003**: Repository MUST contain marketplace metadata files for discovery on MCP server directories.
- **FR-004**: Repository MUST contain MCP client configuration files showing the standard way to connect to the server for development and production use.
- **FR-005**: The server MUST support both stdio transport (for local use) and streamable-http transport (for hosted/remote use and claude.ai connectors).
- **FR-006**: The server MUST require zero mandatory environment variables since it uses only public Tekna data — all configuration MUST be optional.
- **FR-007**: Repository MUST contain a container build file that produces a production-ready image running the server with streamable-http transport by default.
- **FR-008**: The plugin manifest version MUST stay synchronized with the project version defined in the package metadata.
- **FR-009**: Repository MUST provide clear installation instructions for each distribution channel: Claude Code plugin, Claude Desktop config, package registry, and containerized deployment.
- **FR-010**: Repository MUST contain a desktop extension package in `.mcpb` format for one-click Claude Desktop installation.

### Key Entities

- **Plugin Manifest**: Metadata file describing the plugin for Claude Code's plugin system, including name, version, author, and capabilities.
- **Server Manifest**: Registry-format file describing how to install and run the MCP server, including package registry, transport, and runtime requirements.
- **Marketplace Entry**: Metadata for third-party MCP server directories that enables discovery and installation.
- **Client Configuration**: Files showing how to configure MCP clients to connect to the server.
- **Desktop Extension**: A `.mcpb` packaged file that enables one-click installation in Claude Desktop.

## Assumptions

- The Claude Code plugin system uses the `.claude-plugin/plugin.json` format as established by existing plugins.
- The MCP server registry schema follows the standard at `modelcontextprotocol.io`.
- The package will be published to a package registry, installable via standard package runners.
- Container images will be published to a container registry.
- No environment variables are required for basic operation since the server uses only public Tekna endpoints.
- Skills and agents for the plugin are explicitly out of scope for this feature — they can be added as a separate feature later.
- The distribution follows the same patterns established in the mcp-outline project.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new user can install and use the mcp-tekna plugin in Claude Code within 2 minutes using a single command.
- **SC-002**: A Claude Desktop user can configure the server and start querying Tekna data within 5 minutes following the documentation.
- **SC-003**: The plugin appears correctly in at least one MCP server marketplace with accurate metadata.
- **SC-004**: The containerized server starts and accepts connections within 10 seconds of launch.
- **SC-005**: All distribution channels connect to the same server codebase with no channel-specific code forks.
- **SC-006**: Zero mandatory environment variables are required for any distribution channel — the server works out of the box.
