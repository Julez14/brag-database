# Cloud retrieval through MCP

Use Cloudflare's maintained authenticated server at `https://mcp.cloudflare.com/mcp`. It exposes `search` (API schema discovery) and `execute` (API calls). The server's tool named `search` searches API documentation, not personal notes: actually call the instance's search API through `execute`.

Read `cloud.account_id`, `cloud.namespace`, and `cloud.instance_id` from the local configuration. If any is absent, stop cloud retrieval and report the missing configuration. Do not select an account by guessing or searching across unrelated accounts.

Discover the current POST schema for:

```
/accounts/{account_id}/ai-search/namespaces/{name}/instances/{id}/search
```

Then call that endpoint with the configured values, URL-encoding each path segment, and pass the configured account ID to `execute` itself. Current request shape:

```json
{
  "query": "A time I resolved disagreement within a team",
  "ai_search_options": {
    "query_rewrite": {"enabled": false},
    "retrieval": {
      "retrieval_type": "hybrid",
      "max_num_results": 8,
      "context_expansion": 1,
      "keyword_match_mode": "or"
    }
  }
}
```

The instance must have both keyword and vector indexes enabled for hybrid search. Verify the returned API success flag; surface permission, indexing, or configuration failures. An empty result is not proof the user lacks the experience. Try focused paraphrases and exact project names; if evidence remains insufficient, ask for the relevant facts.

Return source text and identifying metadata, not another model's generated answer. Do not call `/chat/completions`. Codex writes the final response.

For full context, use the instance's authenticated item listing/download/chunk APIs after discovering their current schema. Alternatively read the exact source object through authenticated R2 APIs in the configured bucket. Scope requests to the configured prefix. Never expose the R2 bucket or AI Search instance publicly to obtain a citation. Cite the original note's path and section, using an Obsidian link when practical.

A note may be newer in R2 than in the index. If freshness matters, inspect job status and source modification time. The drafting skill may read status but does not provision resources, alter indexing settings, or delete anything. Setup/repair requests authorize a separate configuration workflow.

References:

- [Cloudflare MCP](https://github.com/cloudflare/mcp)
- [AI Search REST search](https://developers.cloudflare.com/ai-search/api/search/rest-api/)
- [AI Search syncing](https://developers.cloudflare.com/ai-search/configuration/indexing/syncing/)
