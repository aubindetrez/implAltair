# Blocks in the Graph:

The full block diagram in inside [./doc/Architecture.odg](doc/Architecture.odg) (LibreOffice Draw document)

## Instruction cache

TODO: Describe the dummy instruction cache once the implementation is done and
verified

TODO: Describe the (normal) instruction cache once the implementation is done and
verified

# Learning resources

## Memory access pattern
<https://en.wikipedia.org/wiki/Memory_access_pattern>
keywords: Random Access, RAM, Gather, Scatter, Strided

## Caches
To learn more about CPU caching:
 - General description of CPU caches: <https://en.wikipedia.org/wiki/CPU_cache>

Keywords: cache enties, cache line, cache block, cache hit, cache miss, 
replacement policies (least-recently used (LRU)), non-cacheable memory ranges,
write policies (write-through, write-back, copy-back, dirty bit, store data queue,
cache coherence policies), associativity (placement policy, fully associative,
direct-mapped, N-way set associative, speculative execution, skewed cache,
pseudo-associative cache, content-addressable memory, hash-rehash cache,
column-associative cache), cache entry (tag, data block flab bits), virtual memory (address translation, memory management unit (MMU), translation lookaside buffer (TLB), page table, segment table, virtual addresses aliasing, granularity, page sizes)... Page coloring, victim cache, trace cache, branch target instruction cache. Inclusive/Exclusive caches, Separate/Unified caches, scratchpad memory (SPM)
 - <https://en.wikipedia.org/wiki/Cache_replacement_policies>
 - <https://en.wikipedia.org/wiki/Page_replacement_algorithm>
 - <https://www.d.umn.edu/~gshute/arch/cache-addressing.xhtml>
 - Cache placement policies: <https://en.wikipedia.org/wiki/Cache_placement_policies>


Caches can contain error correction code: <https://en.wikipedia.org/wiki/ECC_memory#cache>

## Direct mapped caches
 - Direct-mapped (no replacement policy)
 - Skewed (good hash function: TODO )

## Branch target instruction cache

## Other recommanded reading:
 - <https://en.wikipedia.org/wiki/Content-addressable_memory>
 - Computer architecture a quantitative approach.
Keywords: Sequential consistency (SC), release consistency (RC), store order (PSO), Total store order (TSO)
 - CMSO VLSI design, A circuits and systems perspective by Weste and Harris. 
