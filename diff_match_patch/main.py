import diff_match_patch as dmp_module

dmp = dmp_module.diff_match_patch()
diff = dmp.diff_main("Hello World.", "Goodbye World.")
# Result: [(-1, "Hell"), (1, "G"), (0, "o"), (1, "odbye"), (0, " World.")]
dmp.diff_cleanupSemantic(diff)
# Result: [(-1, "Hello"), (1, "Goodbye"), (0, " World.")]
print(diff)

with open('gmp.html', 'w', encoding='utf-8') as f:
    f.write('<html>\n<head>\n<link rel="stylesheet" href="styles.css">\n<title>'+"gmp"+'</title>\n<style>\n.green {color: green;}\n.red {color: red;}\n</style>\n</head>\n<body>\n')
    f.write(f'<h2>test</h2>\n')
    f.write('<div class="para">\n')
    for line in diff:
        print(line)
        if line[0]==0:
            f.write(f'<p>{line[1]}</p>')
        elif line[0]==-1:
            f.write(f'<p class="red"><s>{line[1]}</s></p>')
        elif line[0]==1:
            f.write(f'<p class="green">{line[1]}</p>')
    f.write('</div>\n')
    f.write('</body>\n</html>')