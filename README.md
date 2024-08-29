# Flux Prompt Enhance

Flux Prompt Enhance 是一个用于生成高质量 Prompt 的工具，适用于 ComfyUI 环境。该项目基于 gokaygokay 和 fairy-root 的开源工作，支持在中文语境下生成更符合需求的 Prompt。

## 模型下载与配置

推荐使用 Hugging Face 镜像站进行下载，以确保更快的下载速度。

### 步骤 1: 新建文件夹

在 `ComfyUI_windows_portable\ComfyUI\models\LLM\` 目录下新建文件夹 `Flux-Prompt-Enhance`。  

### 步骤 2: 使用 Windows PowerShell 下载

打开 Windows PowerShell，输入以下命令设置 Hugging Face 镜像站环境变量：

```powershell  
$env:HF_ENDPOINT = "https://hf-mirror.com"
```
接下来，使用 huggingface-cli 命令下载模型至之前创建的文件夹中：
```powershell    
huggingface-cli download --resume-download gokaygokay/Flux-Prompt-Enhance --local-dir .\ComfyUI_windows_portable\ComfyUI\models\LLM\Flux-Prompt-Enhance  
```
请将路径 .\ComfyUI_windows_portable\ComfyUI\models\LLM\Flux-Prompt-Enhance 替换为你自己的文件夹地址。

## 参考资源
- [Flux-Prompt-Generator 源代码](https://github.com/fairy-root/Flux-Prompt-Generator)
- [Hugging Face 模型页面](https://huggingface.co/gokaygokay/Flux-Prompt-Enhance)

## 特别感谢
感谢 gokaygokay 和 fairy-root 的开源贡献，使得此工具得以实现。
