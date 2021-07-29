# Development project 

Building basic game engine and data files for BSF project

## Things to think about

- what if temp goes above maximum temp this code dose not fix this
```
if growth_from_temp < 0:
            growth_from_temp = 0
```
- should a day be a day be added for each growth modifier like at the moment or only one each time it appears even if there is multiple
- if one of the growth modifiers is 0 you waon't grow that day