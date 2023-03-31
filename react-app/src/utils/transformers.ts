import {
  CreateArrayResult,
  DailyProgressionResult,
  MonthlyProgressionStats,
} from "@/types";

export function createArray(data: MonthlyProgressionStats): CreateArrayResult {
  let result = [] as CreateArrayResult;

  for (const date in data) {
    const dayStats = data[date];

    const dayResult = {
      date,
      grand_total: dayStats.grand_total,
      languages: dayStats.languages,
      editors: dayStats.editors,
    };

    result.push(dayResult);
  }

  return result;
}

export function createDailyProgression(
  data: CreateArrayResult
): DailyProgressionResult {
  const dailyProgression = data.map((dayStats) => ({
    name: dayStats.grand_total.text,
    hours: parseFloat(dayStats.grand_total.decimal),
  }));

  return dailyProgression;
}
