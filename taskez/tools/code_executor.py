import math
from typing import Any, Dict
from taskez.tools.base import BaseTool

class CodeCalculatorTool(BaseTool):
    name = "code_calculator"
    description = "Executes sandboxed mathematical expressions, budget/financial computations, and statistical evaluations."

    def _run(self, expression: str, context_vars: Dict[str, Any] = None) -> Dict[str, Any]:
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty.")
            
        clean_expr = expression.strip()
        context_vars = context_vars or {}
        
        # Safe math dictionary
        safe_dict = {
            "math": math,
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "len": len,
            "int": int,
            "float": float,
            "str": str,
            "list": list,
            "dict": dict
        }
        safe_dict.update(context_vars)
        
        # Check for forbidden unsafe statements
        forbidden_keywords = ["import ", "exec(", "eval(", "__", "open(", "os.", "sys.", "subprocess"]
        for kw in forbidden_keywords:
            if kw in clean_expr:
                raise PermissionError(f"Security error: Forbidden statement '{kw}' detected in code expression.")
                
        try:
            # Evaluate expression or simple multi-line script ending with return/val
            if "\n" in clean_expr:
                loc = {}
                exec(clean_expr, safe_dict, loc)
                result_val = loc.get("result", loc)
            else:
                result_val = eval(clean_expr, safe_dict)
                
            return {
                "expression": clean_expr,
                "result": result_val,
                "status": "success"
            }
        except Exception as e:
            raise RuntimeError(f"Calculation/Execution error on expression '{clean_expr}': {str(e)}")
