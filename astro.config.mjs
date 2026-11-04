// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

export default defineConfig({
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],
  },
  integrations: [
    starlight({
      title: 'GATE DA 2027',
      description: 'Topic-wise GATE Data Science & AI notes built from PYQ analysis.',
      customCss: ['katex/dist/katex.min.css', './src/styles/custom.css'],
      lastUpdated: false,
      sidebar: [
        { label: 'Start here', items: ['index', 'roadmap', 'references'] },
        {
          label: 'PDSA (Programming, DS & Algo)',
          items: [
            'pdsa',
            'pdsa/python-semantics',
            'pdsa/recursion-tracing',
            'pdsa/complexity-recurrences',
            'pdsa/searching-sorting',
          ],
        },
      ],
    }),
  ],
});
