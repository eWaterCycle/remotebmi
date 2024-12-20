using RemoteBMI
using Documenter

DocMeta.setdocmeta!(RemoteBMI, :DocTestSetup, :(using RemoteBMI); recursive = true)

const page_rename = Dict("developer.md" => "Developer docs") # Without the numbers
const numbered_pages = [
  file for
  file in readdir(joinpath(@__DIR__, "src")) if file != "index.md" && splitext(file)[2] == ".md"
]

makedocs(;
  modules = [RemoteBMI],
  authors = "",
  repo = "https://github.com/eWaterCycle/remotebmi/blob/{commit}{path}#{line}",
  sitename = "RemoteBMI.jl",
  format = Documenter.HTML(; canonical = "https://eWaterCycle.github.io/remotebmi/RemoteBMI.jl"),
  pages = ["index.md"; numbered_pages],
)
