export interface GrandTotal {
  decimal: string;
  digital: string;
  hours: number;
  minutes: number;
  text: string;
  total_seconds: number;
}

interface Editor extends GrandTotal {
  name: string;
  percent: number;
  seconds: number;
}

interface Language extends Editor {}

interface Machine extends Editor {
  machine_name_id: string;
}

export interface Range {
  date: string;
  end: string;
  start: string;
  text: string;
  timezone: string;
}

interface OperatingSystem extends Editor {}

interface Project extends Editor {}

interface Category extends Editor {}

interface Dependency extends Editor {}

export interface Stats {
  grand_total: GrandTotal;
  editors: Editor[];
  languages: Language[];
  machines?: Machine[];
  range: Range;
  operating_systems: OperatingSystem[];
  projects?: Project[];
  categories?: Category[];
  dependencies?: Dependency[];
}

export interface MonthlyProgressionStats {
  [key: string]: Stats;
}

export type CreateArrayResult = {
  date: string;
  grand_total: GrandTotal;
  languages: Language[];
  editors: Editor[];
}[];

export type DailyProgressionResult = { name: string; hours: number }[];
