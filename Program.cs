using Z.Expressions;
using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.ComponentModel.DataAnnotations;
namespace K_
{
	internal class Program
	{
		static dynamic eval(string expr)
		{
			return Eval.Execute(expr);
		}
		static List<string> split(string input)
		{
			string[] lines = input.Split('\n');
			int j = 0;
			foreach (string line in lines)
			{
				if (line.Contains("#"))
				{
					lines[j] = line.Split("#")[0]; // Remove comments after '#'
				}
				j++;
			}
			string text = string.Join("", lines); // Join lines back into one string

			List<string> res = new List<string>(); // Use List<string> to dynamically store results
			string a = "";
			string type = "str";
			string openm = "([{";
			string closem = ")]}";
			bool escape = false;
			int layer = 0;
			bool in_string = false;
			char string_char = '\x00';

			foreach (char i in text)
			{
				if (escape)
				{
					a += "\\" + i;
					escape = false;
					continue;
				}
				if (i == '\\')
				{
					escape = true;
					continue;
				}
				if (layer == 0)
				{
					if (in_string)
					{
						a += i;
						if (i == string_char)
						{
							res.Add(a); // Add string to the list
							a = "";
							in_string = false;
						}
						continue;
					}
					else if ("\'\"".Contains(i))
					{
						if (a != "")
						{
							res.Add(a); // Add the current value of 'a' before starting a string
						}
						a = Convert.ToString(i);
						in_string = true;
						string_char = i;
					}
					else if (openm.Contains(i))
					{
						if (a != "")
						{
							res.Add(a); // Add 'a' before opening delimiter
						}
						a = Convert.ToString(i);
						layer += 1;
					}
					else if ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".Contains(i))
					{
						if (type == "str")
						{
							a += Convert.ToString(i);
						}
						else
						{
							if (a != "")
							{
								res.Add(a);
							}
							a = Convert.ToString(i);
							type = "str";
						}
					}
					else if ("`~!@#$%^&*-_=+\\|;:\'\",./<>?".Contains(i))
					{
						if (type == "punc")
						{
							a += Convert.ToString(i);
						}
						else
						{
							if (a != "")
							{
								res.Add(a); // Add 'a' before adding punctuation
							}
							a = Convert.ToString(i);
							type = "punc";
						}
					}
					else if (i == ' ')
					{
						if (a != "")
						{
							res.Add(a); // Add 'a' for space separation
						}
						a = "";
					}
					else if (closem.Contains(i))
					{
						throw new Exception("Unexpected closing delimiter");
					}
				}
				else
				{
					a += i;
					if (openm.Contains(i))
					{
						layer += 1;
					}
					else if (closem.Contains(i))
					{
						layer -= 1;
						if (layer == 0)
						{
							res.Add(a); // Add complete group with matching parentheses
							a = "";
							type = "str";
						}
					}
				}
			}
			if (a != "")
			{
				res.Add(a); // Add remaining part of 'a'
			}
			res = res.Where(o => !string.IsNullOrEmpty(o)).ToList(); // Remove empty entries
			return res;
		}
		static Dictionary<string, Tuple<string, string>> toParams(string val)
		{
			string[] vals = val.Trim().Substring(1, val.Length - 2).Split(",");
			Dictionary<string, Tuple<string, string>> res = new();
			foreach (string i in vals)
			{
				string j = i.Trim();
				if (!i.Contains("="))
				{
					res[i] = new Tuple<string, string>("required", "");
				}
				else
				{
					string[] parts = i.Split('=');
					res[parts[0]] = new Tuple<string, string>("optional", parts[1]);
				}
			}
			return res;
		}
		static void Debug(string label, string message = "")
		{
			Console.WriteLine($"{label}: {message}");
		}

		static int find_for(string str, string search)
		{
			int index = 0;
			while ((str.Substring(index, search.Length) != search) && ((index + search.Length) < (str.Length + 1)))
			{
				index += 1;
			}
			if (str.Substring(index, search.Length) != search)
			{
				return -1;
			}
			return index;
		}

		static string DetectAndReplaceFunctions(Dictionary<string, Tuple<Dictionary<string, Tuple<string, string>>, string>> functions, string code, Dictionary<string, object> vars)
		{
			Debug("code3", code);
			var codesplit = split(code); // Assuming split() function is implemented
			int index = 0;

			while (index < codesplit.Count)
			{
				if ("[{(".Contains(codesplit[index][0]))
				{
					string replaced = DetectAndReplaceFunctionsArgs(functions, codesplit[index], vars);
					codesplit[index] = replaced;
				}
				else if (vars.ContainsKey(codesplit[index]))
				{
					index++;
					if (codesplit[index][0] == '[')
					{
						string range_ = codesplit[index];
						var rangeParts = range_.Substring(1, range_.Length - 2).Split(':');
						for (int i = 0; i < rangeParts.Length; i++)
						{
							rangeParts[i] = EvalVars(functions, rangeParts[i], vars).ToString();
						}

						string value = EvalVars(functions, codesplit[index - 1], vars).ToString();
						if (rangeParts.Length == 1)
						{
							value = value[int.Parse(rangeParts[0])].ToString();
						}
						else if (rangeParts.Length == 2)
						{
							value = value.Substring(int.Parse(rangeParts[0]), int.Parse(rangeParts[1]) - int.Parse(rangeParts[0]));
						}
						else if (rangeParts.Length == 3)
						{
							// Implement substring with step if necessary
						}

						code = string.Join("", codesplit);
						code = code.Replace(codesplit[index - 1] + range_, value);
					}
					else
					{
						index--;
					}
				}
				else if (functions.ContainsKey(codesplit[index]))
				{
					string funcName = codesplit[index];
					index++;
					string args = codesplit[index];
					string replace = funcName + args;

					string value = run_function(functions, funcName, args, vars); // Assuming run_function() is implemented
					code = string.Join("", codesplit);
					Debug("replace", replace);
					Debug("replace2", value);
					code = code.Replace(replace, value);
					Debug("replace3", code);
					codesplit = split(code);
				}
				else if (codesplit[index] == "evalp")
				{
					index++;
					string args = codesplit[index];
					string replace = "evalp" + args;

					var value = eval(args.Substring(1, args.Length - 2));
					if (value is string)
					{
						value = $"repr('{value}')";
					}

					code = string.Join("", codesplit).Replace(replace, value.ToString());
					codesplit = split(code);
					index++;
				}

				index++;
			}

			if (codesplit is List<string>)
			{
				code = string.Join("", codesplit);
			}

			Debug("code4", code);
			return code;
		}

		static string DetectAndReplaceFunctionsArgs(Dictionary<string, Tuple<Dictionary<string, Tuple<string, string>>, string>> functions, string args, Dictionary<string, object> vars)
		{
			string a = "";
			if (args.StartsWith("("))
			{
				a = "(" + DetectAndReplaceFunctions(functions, args.Substring(1, args.Length - 2), vars) + ")";
			}
			else if (args.StartsWith("["))
			{
				a = "[" + DetectAndReplaceFunctions(functions, args.Substring(1, args.Length - 2), vars) + "]";
			}
			else if (args.StartsWith("{"))
			{
				a = "{" + DetectAndReplaceFunctions(functions, args.Substring(1, args.Length - 2), vars) + "}";
			}

			return a;
		}

		static string ParseExpr(Dictionary<string, Tuple<Dictionary<string, Tuple<string, string>>, string>> functions, string code, Dictionary<string, object> vars)
		{
			foreach (var variable in vars)
			{
				string pattern = $@"\b{Regex.Escape(variable.Key)}\b";
				code = Regex.Replace(code, pattern, vars[variable.Key].ToString());
			}

			code = DetectAndReplaceFunctions(functions, code, vars);
			return code;
		}

		static dynamic EvalVars(Dictionary<string, Tuple<Dictionary<string, Tuple<string, string>>, string>> functions, string stmt, Dictionary<string, object> vars)
		{
			stmt = ParseExpr(functions, stmt, vars);
			Debug(stmt);
			return eval(stmt).ToString();
		}
		static dynamic run_function(Dictionary<string, Tuple<Dictionary<string, Tuple<string, string>>, string>> functions, string func_name, string args, Dictionary<string, dynamic> vars)
		{
			args = args.Substring(1, args.Length - 2);
			args += "(" + args + ",)";
			List<dynamic> eargs = EvalVars(functions, args, vars);
			Tuple<Dictionary<string, Tuple<string, string>>, string> funcdata = functions[func_name];
			Dictionary<string, Tuple<string, string>> req = funcdata.Item1;
			string func_code = funcdata.Item2;
			Dictionary<string, dynamic> merged = MergeDictWithList(req, eargs);
			merged = MergeDictionary(merged, vars);
			dynamic returnval = 0;
			//dynamic returnval, Dictionary< string, Tuple<Dictionary<string, Tuple<string, string>>, string>> a, Dictionary<string, dynamic> b, int returned = run(func_code, functions, merged);
			return returnval;
		}
		static string detect_and_replace_functions(Dictionary<string, Tuple<Dictionary<string, Tuple<string, string>>, string>> functions, string code, Dictionary<string, dynamic> vars) {
			List<string> code_ = split(code);
			int index = 0;
			string replace = "";
			while (index < code_.Count)
			{
				if ("[({".Contains(code_[index][0])) {
					
				}
			}
		}
		static Dictionary<string, dynamic> MergeDictionary(Dictionary<string, dynamic> a, Dictionary<string, dynamic> b)
		{
			foreach (var kv in b)
			{
				if (!a.ContainsKey(kv.Key)) {
					a[kv.Key] = kv.Value;
				}
			}
			return a;
		}
		static Dictionary<string, dynamic> MergeDictWithList(Dictionary<string, Tuple<string, string>> struct_, List<dynamic> values)
		{
			Dictionary<string, dynamic> res = new Dictionary<string, dynamic>();
			int index = 0;
			foreach (KeyValuePair<string, Tuple<string, string>> arg in struct_)
			{
				//.Key, .Value
				string key = arg.Key;
				(string status, dynamic value) = arg.Value;
				if (status == "required") {
					if (values.Count >= index + 1) {
						res[key] = values[index++];
					}
					else {
						Debug("Error: Not enough args");
						throw new Exception("Not enough args");
					}
				}
				else {
					if (values.Count < index + 1) {
						res[key] = value;
						index++;
					}
					else {
						res[key] = values[index++];
					}
				}
			}
			return res;
		}
		static void Main(string[] args)
		{
			Console.WriteLine("Hello, World!");
			Console.Write("Enter input: ");
			List<string> tokens = split(Console.ReadLine()); // Now returns a List<string>
			foreach (string token in tokens)
			{
				Console.WriteLine(token);
			}
		}
	}
}

