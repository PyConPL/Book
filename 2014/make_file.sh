cp presentations/Optimizing_API_against_latency/cisco.png ./ 
find . -name "text.md" -print | xargs pandoc -o text.pdf --template template.tex -s --toc --toc-depth=1
