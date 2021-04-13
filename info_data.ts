import yahoo_finance from "yahoo-finance2";
import fs = require("fs");
import parse = require("csv-parse/lib/sync.js");

const SYMBOL_FILE_NAME = "./symbols.csv";
const RESULT_FILE_NAME = "./info_data.csv";

const get_csv = (filename) => {
  const file_text = fs.readFileSync(filename, {
    encoding: "utf8",
    flag: "r",
  });

  const csv = parse(file_text, {
    columns: true,
    skip_empty_lines: true,
    delimiter: ";",
  });

  return csv;
};

const get_symbols = (filename) => {
  return get_csv(filename).map((row) => row.upper_case);
};

const get_columns = () => {
  return [
    "symbol",
    "longName",
    "state",
    "country",
    "industry",
    "sector",
    "fullTimeEmployees",
  ];
};

const init_result = (filename, columns) => {
  fs.writeFileSync(filename, columns.join(";") + "\n");
};

// fetch more :
// https://github.com/gadicc/node-yahoo-finance2/blob/0b96e5d1499b50bebeefaedaa94035ed675301e6/docs/modules/quoteSummary.md
const get_info = async (symbol) => {
  const info = await yahoo_finance.quoteSummary(
    symbol,
    {
      modules: ["summaryProfile", "price"],
    },
    { validateResult: false }
  );

  return {
    symbol,
    ...info.summaryProfile,
    ...info.price,
  };
};

const get_row_text = (info, columns) => {
  let row = "";
  for (const key of columns) {
    if (info[key]) {
      row += String(info[key]).replace(/;|\n/g, "");
    }
    row += ";";
  }
  return row.slice(0, -1) + "\n";
};

const fetch_all_data = (filename, symbols, columns) => {
  return new Promise<void>((resolve) => {
    init_result(filename, columns);

    let i = 0;

    const fields = new Set(columns);

    symbols.forEach(async (symbol) => {
      try {
        const info = await get_info(symbol);

        // check missing fields
        const keys = Object.keys(info);
        for (const key of keys) {
          if (!fields.has(key)) {
            fields.add(key);
            console.log(`field missing: ${key}`);
          }
        }

        if (info != null) {
          fs.appendFileSync(filename, get_row_text(info, columns));
        }
      } catch (e) {}

      ++i;
      if (i >= symbols.length) {
        resolve();
      }

      // logs
      if (i % (symbols.length / 10) === 0) {
        console.log(`${i}/${symbols.length}`);
      }
    });
  });
};

const main = async () => {
  const symbols = get_symbols(SYMBOL_FILE_NAME);
  const columns = get_columns();
  await fetch_all_data(RESULT_FILE_NAME, symbols, columns);
};

main().catch(console.log);
