export interface Condition {
  variable: string;
  comparison: string;
  value: number;
  nextComparison: string | null;
}
