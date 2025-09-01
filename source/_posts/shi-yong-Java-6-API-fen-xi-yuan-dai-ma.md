---
title: 使用Java 6 API分析源代码
id: 954
date: 2024-10-31 22:01:47
author: daichangya
excerpt: 静态代码分析工具Checkstyle, FindBugs，以及IDE如NetBeans, Eclipse能快速进行代码关联，它们使用了API解析代码，生成AST，深入分析代码元素。
permalink: /archives/shi-yong-Java-6-API-fen-xi-yuan-dai-ma/
categories:
- java基础
- java源码分析
---

原文：https://blogs.oracle.com/corejavatechtips/source-code-analysis-using-java-6-apis

静态代码分析工具Checkstyle, FindBugs，以及IDE如NetBeans, Eclipse能快速进行代码关联，它们使用了API解析代码，生成AST，深入分析代码元素。JAVA 6 提供了3种新API来完成这样的任务：

[http://www.jcp.org/en/jsr/detail?id=199">Java Compiler API](http://today.java.net/pub/a/today/2008/04/10/%3Cbr)(JSR 199),

[http://www.jcp.org/en/jsr/detail?id=269">Pluggable AnnotationProcessing API](http://today.java.net/pub/a/today/2008/04/10/%3Cbr) (JSR 269)

[http://java.sun.com/javase/6/docs/jdk/api/javac/tree/index.html">CompilerTree API.](http://today.java.net/pub/a/today/2008/04/10/%3Cbr)

在本文中，我们探讨了其中每个 API 的功能，并继续开发一个简单的演示应用程序，来在作为输入提供的一套源码文件上验证特定的 Java 编码规则。此实用程序还显示了编码违规消息以及作为输出的违规源码的位置。考虑一个简单的 Java 类，它覆盖 Object 类的 equals() 方法。要验证的编码规则是实现 equals() 方法的每个类也应该覆盖具有合适签名的 hashcode() 方法。您可以看到下面的 TestClass 类没有定义 hashcode() 方法，即使它具有 equals() 方法。

	public class TestClass implements Serializable {
	 int num;

	 @Override
	  public boolean equals(Object obj) {
			if (this == obj)
					return true;
			if ((obj == null) || (obj.getClass() != this.getClass()))
					return false;
			TestClass test = (TestClass) obj;
			return num == test.num;
	  }
	}

　　让我们继续借助这三个 API 将此类作为构建过程的一部分进行分析。

　　从代码中调用编译器：Java Compiler API

　　我们全部使用 javac 命令行工具来将 Java 源文件编译为类文件。那么我们为什么需要 API 来编译 Java 文件呢?好的，答案极其简单：正如名称所示，这个新的标准 API 告诉我们从自己的 Java 应用程序中调用编译器;比如，可以通过编程方式与编译器交互，从而进行应用程序级别服务的编译部分。此 API 的一些典型使用如下。

　　Compiler API 帮助应用[服务器](http://server.chinaitlab.com/)最小化部署应用程序的时间，例如，避免了使用外部编译器来编译从 JSP 页面中生成的 servlet 源码的开销

　　IDE 等开发人员工具和代码分析器可以从编辑器或构建工具中调用编译器，从而显著降低编译时间。

　　Java Compiler 类包装在 javax.tools 包中。此包的 ToolProvider 类提供了一个名为 getSystemJavaCompiler() 的方法，此方法返回某个实现了 JavaCompiler 接口的类的实例。此编译器实例可用于创建一个将执行实际编译的编译任务。然后，要编译的 Java 源文件将传递给此编译任务。为此，编译器 API 提供了一个名为 JavaFileManager 的文件管理器抽象，它允许从各种来源中检索 Java 文件，比如从文件系统、数据库、内存等。在此示例中，我们使用 StandardFileManager，一个基于 java.io.File 的文件管理器。此标准文件管理器可以通过调用 JavaCompiler 的 getStandardFileManager() 方法来获得。上述步骤的代码段如下所示：

	//Get an instance of java compiler
	JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();

	//Get a new instance of the standard file manager implementation
	StandardJavaFileManager fileManager = compiler.
			getStandardFileManager(null, null, null);
			
	// Get the list of java file objects, in this case we have only 
	// one file, TestClass.java
	Iterable<? extends JavaFileObject> compilationUnits1 = 
			fileManager.getJavaFileObjectsFromFiles("TestClass.java");

　　诊断监听器可以传递给 getStandardFileManager() 方法来生成任何非致命问题的诊断报告。在此代码段中，我们传递 null 值，因为我们准备从此工具中收集诊断。有关传递给这些方法的其他参数的详细信息，请参阅 Java 6 API。StandardJavaFileManager 的 getJavaFileObjectsfromFiles() 方法返回与所提供的 Java 源文件相java JavaFileObject 实例。

　　下一步是创建 Java 编译任务，这可以使用 JavaCompiler 的 getTask() 方法来获得。这时，编译任务尚未启动。此任务可以通过调用 CompilationTask 的 call() 方法来触发。创建和触发编译任务的代码段如下所示。

	// Create the compilation task
	CompilationTask task = compiler.getTask(null, fileManager, null,
											null, null, compilationUnits1);
											
	// Perform the compilation task.
	task.call();

　　假设没有任何编译错误，这将在目标目录中生成 TestClass.class 文件。

　注解处理：可插入的注解处理 API

　　众所周知，Java SE 5.0 引入了在 Java 类、字段、方法等元素中添加和处理元数据或注解的支持。注解通常由构建工具或运行时环境处理以执行有用的任务，比如控制应用程序行为，生成代码等。Java 5 允许对注解数据进行编译时和运行时处理。注解处理器是可以动态插入到编译器中以在其中分析源文件和处理注解的实用程序。注解处理器可以完全利用元数据信息来执行许多任务，包括但不限于下列任务。

　　注解可用于生成部署描述符文件，例如，对于实体类和企业 bean，分别生成 persistence.xml 或 ejb-jar.xml。

　　注解处理器可以使用元数据信息来生成代码。例如，处理器可以生成正确注解的企业 bean 的 Home 和 Remote 接口。

　　注解可用于验证代码或部署单元的有效性。

　　Java 5.0 提供了一个 注解处理工具(Annotation Processing Tool APT) 和一个相关联的基于镜像的反射 API (com.sun.mirror.*)，以处理注解和模拟处理的信息。APT 工具为所提供的 Java 源文件中出现的注解运行相匹配的注解处理器。镜像 API 提供了源文件的编译时只读视图。APT 的主要缺点是它没有标准化;比如，APT 是特定于 Sun JDK 的。

　　Java SE 6 引入了一个新的功能，叫做 可插入注解处理(Pluggable Annotation Processing) 框架，它提供了标准化的支持来编写自定义的注解处理器。之所以称为“可插入”，是因为注解处理器可以动态插入到 javac 中，并可以对出现在 Java 源文件中的一组注解进行操作。此框架具有两个部分：一个用于声明注解处理器并与其交互的 API -- 包 javax.annotation.processing -- 和一个用于对 Java 编程语言进行建模的 API -- 包 javax.lang.model。

　　编写自定义注解处理器

　　下一节解释如何编写自定义注解处理器，并将其插入到编译任务中。自定义注解处理器继承 AbstractProcessor(这是 Processor 接口的默认实现)，并覆盖 process() 方法。

　　注解处理器类将使用两个类级别的注解 @SupportedAnnotationTypes 和 @SupportedSourceVersion 来装饰。 SupportedSourceVersion 注解指定注解处理器支持的最新的源版本。SupportedAnnotationTypes 注解指示此特定的注解处理器对哪些注解感兴趣。例如，如果处理器只需处理 Java Persistence API (JPA) 注解，则将使用 @SupportedAnnotationTypes ("javax.persistence.*")。值得注意的一点是，如果将支持的注解类型指定为 @SupportedAnnotationTypes("*")，即使没有任何注解，仍然会调用注解处理器。这允许我们有效利用建模 API 以及 Tree API 来执行通用的源码处理。使用这些 API，可以获得与修改符、字段、方法但等有关的大量有用的信息。自定义注解处理器的代码段如下所示：

	@SupportedSourceVersion(SourceVersion.RELEASE_6)
	@SupportedAnnotationTypes("*")
	public class CodeAnalyzerProcessor extends AbstractProcessor {
		@Override
		public boolean process(Set<? extends TypeElement> annotations,
				RoundEnvironment roundEnvironment) {
			for (Element e : roundEnvironment.getRootElements()) {
					System.out.println("Element is "+ e.getSimpleName());
					// Add code here to analyze each root element
			}
			return true;
		}
	}

　　是否调用注解处理器取决于源码中存在哪些注解，哪些处理器配置为可用，哪些注解类型是可用的后处理器进程。注解处理可能发生在多个轮回中。例如，在第一个轮回中，将处理原始输入 Java 源文件;在第二个轮回中，将考虑处理由第一个轮回生成的文件，等等。自定义处理器应覆盖 AbstractProcessor 的 process()。此方法接受两个参数：

　　源文件中找到的一组 TypeElements/ 注解。

　　封装有关注解处理器当前处理轮回的信息的 RoundEnvironment。

　　如果处理器声明其支持的注解类型，则 process() 方法返回 true，而不会为这些注解调用其他处理器。否则，process() 方法返回 false 值，并将调用下一个可用的处理器(如果存在的话)。

　　插入到注解处理器中

　　既然自定义注解处理器已经可供使用，现在让我们来看如何作为编译过程的一部分来调用此处理器。此处理器可以通过 javac 命令行实用程序或以编程方式通过独立 Java 类来调用。Java SE 6 的 javac 实用程序提供一个称为 -processor 的选项，来接受要插入到的注解处理器的完全限定名。语法如下：

　	javac -processor demo.codeanalyzer.CodeAnalyzerProcessor TestClass.java

　　其中 CodeAnalyzerProcessor 是注解处理器类，TestClass 是要处理的输入 Java 文件。此实用程序在类路径中搜索 CodeAnalyzerProcessor;因此，一定要将此类放在类路径中。

　　以编程方式插入到处理器中的修改后的代码段如下。CompilationTask 的 setProcessors() 方法允许将多个注解处理器插入到编译任务中。此方法需要在 call() 方法之前调用。还要注意，如果注解处理器插入到编译任务中，则注解处理首先发生，然后才是编译任务。不用说，如果代码导致编译错误，则注解处理将不会发生。

	CompilationTask task = compiler.getTask(null, fileManager, null,
											null, null, compilationUnits1);
											
	// Create a list to hold annotation processors
	LinkedList<AbstractProcessor> processors = new LinkedList<AbstractProcessor>();

	// Add an annotation processor to the list
	processors.add(new CodeAnalyzerProcessor());

	// Set the annotation processor to the compiler task
	task.setProcessors(processors);

	// Perform the compilation task.
	task.call();

　　如果执行上述代码，它将导致注解处理器在用于打印名称“TestClass”的 TestClass.java 的编译期间启动。

　访问抽象语法树：Compiler Tree API

　　抽象语法树(Abstract Syntax Tree)是将 Java 表示为节点树的来源的只读视图，其中每个节点表示一个 Java 编程语言构造或树，每个节点的子节点表示这些树有意义的组件。例如，Java 类表示为 ClassTree，方法声明表示为 MethodTree，变量声明表示为 VariableTree，注解表示为 AnnotationTree，等等。

　　Compiler Tree API 提供 Java 源码的抽象语法树(Abstract Syntax Tree)，还提供 TreeVisitor、TreeScanner 等实用程序来在 AST 上执行操作。对源码内容的进一步分析可以使用 TreeVisitor 来完成，它访问所有子树节点以提取有关字段、方法、注解和其他类元素的必需信息。树访问器以访问器设计模式的风格来实现。当访问器传递给树的接受方法时，将调用此树最适用的 visitXYZ 方法。

　　Java Compiler Tree API 提供 TreeVisitor 的三种实现;即 SimpleTreeVisitor、 TreePathScanner 和 TreeScanner。演示应用程序使用 TreePathScanner 来提取有关 Java 源文件的信息。 TreePathScanner 是访问所有子树节点并提供对维护父节点路径的支持的 TreeVisitor。需要调用 TreePathScanner 的 scan() 方法才能遍历树。要访问特定类型的节点，只需覆盖相应的 visitXYZ 方法。在访问方法中，调用 super.visitXYZ 以访问后代节点。典型访问器类的代码段如下：

	public class CodeAnalyzerTreeVisitor extends TreePathScanner<Object, Trees>  {
		@Override
		public Object visitClass(ClassTree classTree, Trees trees) {
			---- some code ----
			return super.visitClass(classTree, trees);
		}
		@Override
		public Object visitMethod(MethodTree methodTree, Trees trees) {
			---- some code ----
			return super.visitMethod(methodTree, trees);
		}
	}

　　可以看到访问方法接受两个参数：表示节点的树(ClassTree 表示类节点)，MethodTree 表示方法节点，等)，和 Trees 对象。Trees 类提供用于提取树中元素信息的实用程序方法。必须注意，Trees 对象是 JSR 269 和 Compiler Tree API 之间的桥梁。在本例中，只有一个根元素，即 TestClass 本身。

	CodeAnalyzerTreeVisitor visitor = new CodeAnalyzerTreeVisitor();

	@Override
	public void init(ProcessingEnvironment pe) {
			super.init(pe);
			trees = Trees.instance(pe);
	}
	for (Element e : roundEnvironment.getRootElements()) {
			TreePath tp = trees.getPath(e);
			// invoke the scanner
			visitor.scan(tp, trees);
	}

　　下一节介绍使用 Tree API 来检索源码信息，并填充将来用于代码验证的通用模型。不管何时在使用 ClassTrees 作为参数的 AST 中访问类、接口或枚举类型，都会调用 visitClass() 方法。同样地，对于使用 MethodTree 作为参数的所有方法，调用 visitMethod() 方法，对于使用 VariableTree 作为参数的所有变量，调用 visitVariable()，等等。

	@Override
	public Object visitClass(ClassTree classTree, Trees trees) {
			 //Storing the details of the visiting class into a model
			 JavaClassInfo clazzInfo = new JavaClassInfo();

			// Get the current path of the node     
			TreePath path = getCurrentPath();

			//Get the type element corresponding to the class
			TypeElement e = (TypeElement) trees.getElement(path);

			//Set qualified class name into model
			clazzInfo.setName(e.getQualifiedName().toString());

			//Set extending class info
			clazzInfo.setNameOfSuperClass(e.getSuperclass().toString());

			//Set implementing interface details
			for (TypeMirror mirror : e.getInterfaces()) {
					clazzInfo.addNameOfInterface(mirror.toString());
			}
			return super.visitClass(classTree, trees);
	  }

　　此代码段中使用的 JavaClassInfo 是用于[存储](http://www.storworld.com/)有关 Java 代码的信息的自定义模型。执行此代码之后，与类有关的信息，比如完全限定的类名称、超类名称、由 TestClass 实现的接口等，被提取并[存储](http://www.storworld.com/)在自定义模型中以供将来验证。

  

设置源码位置

　　到目前为止，我们一直在忙于获取有关 AST 各种节点的信息，并填充类、方法和字段信息的模型对象。使用此信息，我们可以验证源码是否遵循好的编程实践，是否符合规范等。此信息对于 Checkstyle 或 FindBugs 等验证工具十分有用，但它们可能还需要有关违反此规则的源码令牌的位置详细信息，以便将错误位置详细信息提供给用户。

　　SourcePositions 对象是 Compiler Tree API 的一部分，用于维护编译单位树中所有 AST 节点的位置。此对象提供有关文件中 ClassTree、MethodTree、 FieldTree 等树的开始位置和结束位置的有用信息。位置定义为从 CompilationUnit 开始位置开始的简单字符偏移，其中第一个字符位于偏移 0。下列代码段显示如何获得传递的 Tree 树从编译单位开始位置开始的字符偏移位置。

	public static LocationInfo getLocationInfo(Trees trees, 
													TreePath path, Tree tree) {
			LocationInfo locationInfo = new LocationInfo();
			SourcePositions sourcePosition = trees.getSourcePositions();
			long startPosition = sourcePosition.
							getStartPosition(path.getCompilationUnit(), tree);
			locationInfo.setStartOffset((int) startPosition);
			return locationInfo;
	}

　　但是，如果我们需要获得提供类或方法本身名称的令牌的位置，则这些信息将不够。要查找源码中的实际令牌位置，一个选项是搜索源码文件中 char 内容内的令牌。我们可以从与如下所示编译单位相应的 JavaFileObject 中获取 char 内容。

	//Get the compilation unit tree from the tree path
	CompilationUnitTree compileTree = treePath.getCompilationUnit();

	//Get the java source file which is being processed
	JavaFileObject file = compileTree.getSourceFile();

	// Extract the char content of the file into a string
	String javaFile = file.getCharContent(true).toString();

	//Convert the java file content to a  character buffer
	CharBuffer charBuffer = CharBuffer.wrap (javaFile.toCharArray());

　　下列代码段查找源码中类名称令牌的位置。java.util.regex.Pattern 和 java.util.regex.Matcher 类用于获取类名称令牌的实际位置。Java 源码的内容使用 java.nio.CharBuffer 转换为字符缓冲器。匹配器从编译单位树中类树的开始位置开始，搜索字符缓冲器中与类名相匹配的令牌的第一次出现。

	LocationInfo clazzNameLoc = (LocationInfo) clazzInfo.
							getLocationInfo();
	int startIndex = clazzNameLoc.getStartOffset();
	int endIndex = -1;
	if (startIndex >= 0) {
	   String strToSearch = buffer.subSequence(startIndex, 
	   buffer.length()).toString();
	   Pattern p = Pattern.compile(clazzName);
	   Matcher matcher = p.matcher(strToSearch);
	   matcher.find();
	   startIndex = matcher.start() + startIndex;
	   endIndex = startIndex + clazzName.length();
	  } 
	clazzNameLoc.setStartOffset(startIndex);
	clazzNameLoc.setEndOffset(endIndex);
	clazzNameLoc.setLineNumber(compileTree.getLineMap().
				  getLineNumber(startIndex));

　　Complier Tree API 的 LineMap 类提供 CompilationUnitTree 中字符位置和行号的映射。我们可以通过将开始偏移位置传递给 CompilationUnitTree 的 getLineMap() 方法来获取所关注令牌的行号。

　　按照规则验证源码

　　既然已经从 AST 中成功检索了所需的信息，下一个任务就是验证所考虑的源码是否满足预定义的编码标准。编码规则在 XML 文件中配置，并由名为 RuleEngine 的自定义类管理。此类从 XML 文件中提取规则，并一个一个地将其启动。如果此类不满足某个规则，则此规则将返回 ErrorDescription 对象的列表。 ErrorDescription 对象封装错误消息和错误在源码中的位置。

	ClassFile clazzInfo = ClassModelMap.getInstance().
					getClassInfo(className);
	for (JavaCodeRule rule : getRules()) {
			// apply rules one by one
			Collection<ErrorDescription> problems = rule.execute(clazzInfo);
			if (problems != null) {
					problemsFound.addAll(problems);
			}
	}

　　每个规则实现为 Java 类;要验证的类的模型信息传递给此类。规则类封装逻辑以使用此模型信息验证规则逻辑。示例规则 (OverrideEqualsHashCode) 的实现如下所示。此规则规定覆盖 equal() 方法的类还应该覆盖 hashcode() 方法。在此，我们遍历类的方法并检查它是否遵循 equals() 和 hashcode() 合同。在 TestClass 中，hashcode() 方法不存在，而 equals() 方法存在，从而导致规则返回 ErrorDescription 模型，其中包含适当的错误消息和错误的位置详细信息。

	public class OverrideEqualsHashCode extends JavaClassRule {
		@Override
		protected Collection<ErrorDescription> apply(ClassFile clazzInfo) {
			boolean hasEquals = false;
			boolean hasHashCode = false;
			Location errorLoc = null;
			for (Method method : clazzInfo.getMethods()) {
				String methodName = method.getName();
				ArrayList paramList = (ArrayList) method.getParameters();
				if ("equals".equals(methodName) && paramList.size() == 1) {
					if ("java.lang.Object".equals(paramList.get(0))) {
						hasEquals = true;
						errorLoc = method.getLocationInfo();
					}
				} else if ("hashCode".equals(methodName) &&
					method.getParameters().size() == 0) {
					hasHashCode = true;
				}
			}
			if (hasEquals) {
				if (hasHashCode) {
					return null;
				} else {
					StringBuffer errrMsg = new StringBuffer();
					errrMsg.append(CodeAnalyzerUtil.
									getSimpleNameFromQualifiedName(clazzInfo.getName()));
					errrMsg.append(" : The class that overrides 
											equals() should ");
					errrMsg.append("override hashcode()");
					Collection<ErrorDescription> errorList = new 
													ArrayList<ErrorDescription>();
					errorList.add(setErrorDetails(errrMsg.toString(), 
															errorLoc));
					return errorList;
				}
			}
			return null;
		}
	}

　　运行样例

　　可以从 参考资料 部分中[下载](http://download.chinaitlab.com/)此演示应用程序的二进制文件。将此文件保存到任何本地目录中。在命令提示符中使用下列命令执行此应用程序：

　　	java -classpath \lib\tools.jar;.; demo.codeanalyzer.main.Main

　　结束语

　　本文讨论如何使用新 Java 6 API 来从源码中调用编译器，如何使用可插入的注解处理器和树访问器来解析和分析源码。使用标准 Java API 而非特定于 IDE 的解析/分析逻辑使得代码可以在不同的工具和环境之间重用。我们在此只粗略描绘了与编译器相关的三个 API 的表面;您可以通过进一步深入这些 API 来找到其他许多更有用的功能。