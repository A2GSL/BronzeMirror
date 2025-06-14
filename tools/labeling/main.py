"""
main.py - BronzeMirror标注工具总入口

- 支持命令行批量抓取、自动标注、人工校正、校验与导出
- 可集成Web UI、批量数据处理等功能
"""
import argparse
from core.auto_labeler import AutoLabeler
from core.correction_ui import CorrectionUI
from core.validator import OntologyValidator
from utils.data_loader import DataLoader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BronzeMirror 本体标注工具入口")
    parser.add_argument('--mode', choices=['batch', 'ui', 'validate', 'fetch'], default='ui', help='运行模式：batch批量标注，ui人工校正，validate一致性校验，fetch批量抓取')
    parser.add_argument('--input', type=str, help='输入文件或在线目录URL')
    parser.add_argument('--output', type=str, help='输出文件')
    args = parser.parse_args()

    if args.mode == 'ui':
        CorrectionUI.launch_web_ui()
    elif args.mode == 'batch':
        if not args.input or not args.output:
            print('请指定--input和--output文件')
        else:
            texts = DataLoader.load_txt(args.input)
            results = AutoLabeler.batch_label(texts)
            import json
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f'[INFO] 批量标注结果已保存到 {args.output}')
    elif args.mode == 'validate':
        import json
        if not args.input:
            print('请指定--input标注结果json文件')
        else:
            with open(args.input, encoding='utf-8') as f:
                data = json.load(f)
            issues = OntologyValidator.check_consistency(data)
            OntologyValidator.export_validation_report(issues)
    elif args.mode == 'fetch':
        if not args.input or not args.output:
            print('请指定--input在线目录URL和--output输出json文件')
        else:
            chapters = DataLoader.fetch_all_chapters(args.input)
            import json
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(chapters, f, ensure_ascii=False, indent=2)
            print(f'[INFO] 已抓取章节并保存到 {args.output}')