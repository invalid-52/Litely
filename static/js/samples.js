/**
 * LITELY Curated Code Samples
 */

export const CODE_SAMPLES = {
  python: {
    language: 'python',
    filename: 'rate_limiter.py',
    theme: 'github-dark',
    code: `import time
from collections import deque

class TokenBucket:
    """Thread-safe rate limiter with burst capability."""
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()

    def consume(self, amount: int = 1) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= amount:
            self.tokens -= amount
            return True
        return False`,
  },
  typescript: {
    language: 'typescript',
    filename: 'transformer.ts',
    theme: 'dracula',
    code: `export interface Node<T> {
  id: string;
  value: T;
  next?: Node<T>;
}

export class Pipeline<T, R> {
  private steps: Array<(input: any) => any> = [];

  use<Next>(fn: (input: R) => Next): Pipeline<T, Next> {
    this.steps.push(fn);
    return this as any;
  }

  async execute(initial: T): Promise<R> {
    return this.steps.reduce(
      async (acc, step) => step(await acc),
      Promise.resolve(initial)
    );
  }
}`,
  },
  rust: {
    language: 'rust',
    filename: 'concurrent_cache.rs',
    theme: 'tokyo-night',
    code: `use std::collections::HashMap;
use std::sync::{Arc, RwLock};

#[derive(Clone)]
pub struct Cache<K, V> {
    store: Arc<RwLock<HashMap<K, V>>>,
}

impl<K: Eq + std::hash::Hash + Clone, V: Clone> Cache<K, V> {
    pub fn new() -> Self {
        Self { store: Arc::new(RwLock::new(HashMap::new())) }
    }

    pub fn get(&self, key: &K) -> Option<V> {
        self.store.read().ok()?.get(key).cloned()
    }

    pub fn set(&self, key: K, val: V) {
        if let Ok(mut lock) = self.store.write() {
            lock.insert(key, val);
        }
    }
}`,
  },
  sql: {
    language: 'sql',
    filename: 'analytics_query.sql',
    theme: 'nord',
    code: `WITH monthly_retention AS (
    SELECT
        user_id,
        DATE_TRUNC('month', created_at) AS signup_month,
        DATE_TRUNC('month', active_date) AS activity_month
    FROM user_activity_log
    WHERE active_date >= NOW() - INTERVAL '12 months'
)
SELECT
    signup_month,
    COUNT(DISTINCT user_id) AS cohort_size,
    ROUND(COUNT(DISTINCT user_id) FILTER (
        WHERE activity_month = signup_month + INTERVAL '1 month'
    ) * 100.0 / COUNT(DISTINCT user_id), 2) AS m1_retention_pct
FROM monthly_retention
GROUP BY signup_month
ORDER BY signup_month DESC;`,
  },
  javascript: {
    language: 'javascript',
    filename: 'event_emitter.js',
    theme: 'one-dark',
    code: `class AsyncEmitter {
  #events = new Map();

  on(event, handler) {
    if (!this.#events.has(event)) this.#events.set(event, new Set());
    this.#events.get(event).add(handler);
    return () => this.#events.get(event)?.delete(handler);
  }

  async emit(event, payload) {
    const handlers = Array.from(this.#events.get(event) || []);
    return Promise.all(handlers.map(fn => fn(payload)));
  }
}`,
  },
  go: {
    language: 'go',
    filename: 'worker_pool.go',
    theme: 'catppuccin-mocha',
    code: `package main

import (
	"context"
	"fmt"
	"sync"
)

type Job func(ctx context.Context) error

func RunWorkerPool(ctx context.Context, workers int, jobs <-chan Job) {
	var wg sync.WaitGroup
	for i := 0; i < workers; i++ {
		wg.Add(1)
		go func(id int) {
			defer wg.Done()
			for job := range jobs {
				if err := job(ctx); err != nil {
					fmt.Printf("Worker %d failed: %v\\n", id, err)
				}
			}
		}(i)
	}
	wg.Wait()
}`,
  },
};
