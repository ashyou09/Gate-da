// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// [sidebar label, folder in src/content/docs] — keep in sync with scripts/subjects.json
const subjects = [
  ['Programming, DS & Algorithms', 'pdsa'],
  ['Machine Learning', 'machine-learning'],
  ['DBMS & Warehousing', 'dbms'],
  ['Artificial Intelligence', 'ai'],
  ['Probability & Statistics', 'probability-statistics'],
  ['Linear Algebra', 'linear-algebra'],
  ['Calculus & Optimization', 'calculus-optimization'],
  ['General Aptitude', 'general-aptitude'],
];

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
        // One group per subject, in study order. Pages inside a group come from
        // src/content/docs/<folder>/ automatically, sorted by `sidebar.order`.
        ...subjects.map(([label, directory]) => ({
          label,
          collapsed: directory !== 'pdsa',
          items: [{ autogenerate: { directory } }],
        })),
      ],
    }),
  ],
});
