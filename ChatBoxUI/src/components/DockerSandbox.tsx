import Docker from 'dockerode';

export class DockerSandbox {
  private docker: Docker;
  
  constructor() {
    this.docker = new Docker();
  }
  
  async executeCode(
    code: string, 
    language: string
  ): Promise<{ output: string; exitCode: number }> {
    // create container
    const container = await this.docker.createContainer({
      Image: `code-sandbox:${language}`,
      Cmd: this.getCommand(language),
      AttachStdout: true,
      AttachStderr: true,
      NetworkDisabled: true,
      HostConfig: {
        Memory: 128 * 1024 * 1024, // 128MB
        NanoCpus: 500000000, // 50% CPU
        PidsLimit: 50,
        ReadonlyRootfs: true,
      }
    });
    
    // copy code into container 
    await this.copyCodeToContainer(container, code, language);
    
    // run with timeout
    await container.start();
    
    const stream = await container.logs({
      stdout: true,
      stderr: true,
      follow: true
    });
    
    let output = '';
    stream.on('data', (chunk) => {
      output += chunk.toString();
    });
    
    const result = await container.wait();
    await container.remove();
    
    return {
      output: output.trim(),
      exitCode: result.StatusCode
    };
  }

  // tells container how to run copied code
  
  private getCommand(language: string): string[] {
    const commands: Record<string, string[]> = {
      python: ['python', '/tmp/main.py'],
      javascript: ['node', '/tmp/main.js'],
      typescript: ['ts-node', '/tmp/main.ts'],
      cpp: ['/bin/sh', '/run.sh']
    };
    return commands[language] || commands.cpp;
  }
  
  private async copyCodeToContainer(
    container: Docker.Container,
    code: string,
    language: string
  ): Promise<void> {
    // TODO
  }
}