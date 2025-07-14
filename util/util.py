from datetime import datetime


def dump_all_elements(driver):
    """
    递归遍历页面和所有iframe中的所有元素，
    生成定位信息并写入/tmp/locate.txt
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # 存储已处理的元素和iframe，避免重复
    processed_elements = set()
    processed_iframes = set()

    # 存储结果
    output = []

    def get_element_identifier(elem):
        """生成元素的唯一标识符，用于去重"""
        try:
            tag = elem.tag_name
            id_attr = elem.get_attribute('id') or ''
            class_attr = elem.get_attribute('class') or ''
            text = elem.text.strip()[:20] or ''
            return f"{tag}_{id_attr}_{class_attr}_{text}"
        except:
            return None  # 发生异常时返回None

    def get_element_locator(elem):
        """生成元素的推荐定位方式"""
        try:
            # 1. 优先使用ID
            if (elem_id := elem.get_attribute('id')):
                return f'By.ID, "{elem_id}"'

            # 2. 使用data-sentry-element属性
            if (data_sentry := elem.get_attribute('data-sentry-element')):
                return f'By.XPATH, "//*[@data-sentry-element=\\"{data_sentry}\\"]"'

            # 3. 使用稳定的class（单一类名）
            classes = elem.get_attribute('class')
            if classes and len(classes.split()) == 1:
                return f'By.CSS_SELECTOR, ".{classes}"'

            # 4. 使用文本内容（如果有）
            text = elem.text.strip()
            if text:
                return f'By.XPATH, "//*[contains(., \\"{text}\\")]"'

            # 5. 兜底：使用标签和位置
            tag = elem.tag_name
            return f'By.XPATH, "//{tag}[{len(processed_elements) + 1}]"'

        except:
            return '定位方式生成失败'

    def process_elements(current_driver, context="主页面", depth=0):
        """处理当前上下文中的所有元素，并递归处理iframe"""
        indent = "  " * depth
        output.append(f"\n{indent}[{context}]")
        output.append(f"{indent}{'-' * 50}")

        # 获取当前上下文中的所有元素
        elements = current_driver.find_elements(By.XPATH, "//*")

        for elem in elements:
            try:
                # 生成唯一标识符并检查是否已处理
                identifier = get_element_identifier(elem)
                if not identifier or identifier in processed_elements:
                    continue
                processed_elements.add(identifier)

                # 获取元素信息
                tag = elem.tag_name
                text = elem.text.strip()[:50]  # 限制文本长度
                locator = get_element_locator(elem)

                # 添加到输出
                output.append(f"{indent}元素: {tag}")
                output.append(f"{indent}  文本: {text if text else '无'}")
                output.append(f"{indent}  定位: {locator}")
                output.append(f"{indent}{'-' * 30}")

            except Exception as e:
                output.append(f"{indent}获取元素信息失败: {str(e)}")

        # 处理iframe
        iframes = current_driver.find_elements(By.TAG_NAME, "iframe")
        for i, iframe in enumerate(iframes):
            try:
                # 获取iframe信息
                iframe_id = iframe.get_attribute('id') or f"iframe_{i}"
                iframe_src = iframe.get_attribute('src') or "无src"

                # 检查是否已处理过
                iframe_identifier = f"{iframe_id}_{iframe_src}"
                if iframe_identifier in processed_iframes:
                    continue
                processed_iframes.add(iframe_identifier)

                # 切换到iframe并递归处理
                current_driver.switch_to.frame(iframe)
                iframe_context = f"{context} > iframe#{i} ({iframe_id})"
                process_elements(current_driver, iframe_context, depth + 1)
                current_driver.switch_to.parent_frame()

            except Exception as e:
                output.append(f"{indent}处理iframe失败: {str(e)}")

    # 主程序执行
    try:
        output.append("=" * 50)
        output.append("开始收集页面元素定位信息")
        output.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"URL: {driver.current_url}")
        output.append("=" * 50)

        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # 开始处理主页面
        process_elements(driver)

        output.append("\n" + "=" * 50)
        output.append(f"元素收集完成，共处理 {len(processed_elements)} 个元素")
        output.append("=" * 50)

        # 写入文件
        with open("/tmp/locate.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(output))

        print(f"元素定位信息已成功写入 /tmp/locate.txt")

    except Exception as e:
        print(f"执行过程中发生错误: {str(e)}")
        # 仍然尝试写入已收集的信息
        with open("/tmp/locate.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(output + [f"\n错误: {str(e)}"]))