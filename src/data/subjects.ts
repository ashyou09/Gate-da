import raw from '../../scripts/subjects.json';

export type Priority = 'high' | 'med' | 'low';
export interface Topic {
  title: string;
  priority: Priority;
  page?: string;
  pyqs?: number;
  blurb?: string;
}
export interface Subject {
  slug: string;
  name: string;
  short: string;
  order: number;
  marks: [number, number, number];
  syllabus: string;
  note: string;
  topics: Topic[];
}

export const subjects = (raw as Subject[]).slice().sort((a, b) => a.order - b.order);
export const bySlug = new Map(subjects.map((s) => [s.slug, s]));

export const PRIORITY_LABEL: Record<Priority, string> = {
  high: 'High priority',
  med: 'Medium',
  low: 'Low',
};

/** GATE 2027 first exam day (IIT Madras): 6 Feb 2027, forenoon session, IST. */
export const EXAM_DATE = '2027-02-06T09:30:00+05:30';

export const mean = (m: number[]) => Math.round((m.reduce((a, b) => a + b, 0) / m.length) * 10) / 10;

/** Topics whose page exists in the docs collection. */
export function writtenTopics(s: Subject, ids: Set<string>) {
  return s.topics.filter((t) => t.page && ids.has(`${s.slug}/${t.page}`));
}
