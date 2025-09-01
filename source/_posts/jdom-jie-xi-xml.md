---
title: jdom解析xml
id: 777
date: 2024-10-31 22:01:46
author: daichangya
excerpt: A typical Java application is a domain-specific XML editornobody wants to
  write the markup by handgeneral-purpose XML editors are too clunkyWe generalize
  the business card language to allow col
permalink: /archives/jdom-jie-xi-xml/
tags:
- xml
---


- nobody wants to write the markup by hand- general-purpose XML editors are too clunky

<table class="data" border="" style="background-color:rgb(204,204,255)">
<tbody>
<tr>
<td style="font-family:sans-serif">
<pre style="font-family:'Courier New',Courier,monospace; font-weight:bold; margin-bottom:0px">&lt;cards&gt;
  &lt;card&gt;
    &lt;name&gt;John Doe&lt;/name&gt;
    &lt;title&gt;CEO, Widget Inc.&lt;/title&gt;
    &lt;email&gt;john.doe@widget.com&lt;/email&gt;
    &lt;phone&gt;(202) 456-1414&lt;/phone&gt;
    &lt;logo url=&quot;widget.gif&quot; /&gt;
  &lt;/card&gt;
  &lt;card&gt;
    &lt;name&gt;Michael Schwartzbach&lt;/name&gt;
    &lt;title&gt;Associate Professor&lt;/title&gt;
    &lt;email&gt;mis@brics.dk&lt;/email&gt;
    &lt;phone&gt;&#43;45 8610 8790&lt;/phone&gt;
    &lt;logo url=&quot;http://www.brics.dk/~mis/portrait.gif&quot; /&gt;
  &lt;/card&gt;
  &lt;card&gt;
    &lt;name&gt;Anders Møller&lt;/name&gt;
    &lt;title&gt;Research Assistant Professor&lt;/title&gt;
    &lt;email&gt;amoeller@brics.dk&lt;/email&gt;
    &lt;phone&gt;&#43;45 8942 3475&lt;/phone&gt;
    &lt;logo url=&quot;http://www.brics.dk/~amoeller/am.jpg&quot;/&gt;
  &lt;/card&gt;
&lt;/cards&gt;
</pre>
</td>
</tr>
</tbody>
</table>


We then write a Java&nbsp;[program](http://cs.au.dk/~amoeller/XML/programming/BCedit.java)&nbsp;to edit such collections.

First, we need a high-level representation of a business card:


<table class="code" border="" style="background-color:rgb(255,255,204)">
<tbody>
<tr>
<td style="font-family:sans-serif">
<pre style="font-family:'Courier New',Courier,monospace; font-weight:bold; margin-bottom:0px">class Card {
  public String name, title, email, phone, logo;

  public Card(String name, String title, String email, String phone, String logo) {
    this.name = name;
    this.title = title;
    this.email = email;
    this.phone = phone;
    this.logo = logo;
  }
}
</pre>
</td>
</tr>
</tbody>
</table>


An XML document must then be translated into a vector of such objects:


<table class="code" border="" style="background-color:rgb(255,255,204)">
<tbody>
<tr>
<td style="font-family:sans-serif">
<pre style="font-family:'Courier New',Courier,monospace; font-weight:bold; margin-bottom:0px">Vector doc2vector(Document d) {
  Vector v = new Vector();
  Iterator i = d.getRootElement().getChildren().iterator();
  while (i.hasNext()) {
    Element e = (Element)i.next();
    String phone = e.getChildText(&quot;phone&quot;);
    if (phone==null) phone=&quot;&quot;;
    Element logo = e.getChild(&quot;logo&quot;);
    String url;
    if (logo==null) url = &quot;&quot;; else url = logo.getAttributeValue(&quot;url&quot;);
    Card c = new Card(e.getChildText(&quot;name&quot;),  // exploit schema,
                      e.getChildText(&quot;title&quot;), // assume validity
                      e.getChildText(&quot;email&quot;),
                      phone,
                      url);
    v.add(c);
  }
  return v;
}
</pre>
</td>
</tr>
</tbody>
</table>


And back into an XML document:


<table class="code" border="" style="background-color:rgb(255,255,204)">
<tbody>
<tr>
<td style="font-family:sans-serif">
<pre style="font-family:'Courier New',Courier,monospace; font-weight:bold; margin-bottom:0px">Document vector2doc() {
  Element cards = new Element(&quot;cards&quot;);
  for (int i=0; i&lt;cardvector.size(); i&#43;&#43;) {
    Card c = (Card)cardvector.elementAt(i);
    if (c!=null) {
      Element card = new Element(&quot;card&quot;);
      Element name = new Element(&quot;name&quot;);
      name.addContent(c.name);
      card.addContent(name);
      Element title = new Element(&quot;title&quot;);
      title.addContent(c.title);
      card.addContent(title);
      Element email = new Element(&quot;email&quot;);
      email.addContent(c.email);
      card.addContent(email);
      if (!c.phone.equals(&quot;&quot;)) {
        Element phone = new Element(&quot;phone&quot;);
        phone.addContent(c.phone);
        card.addContent(phone);
      }
      if (!c.logo.equals(&quot;&quot;)) {
        Element logo = new Element(&quot;logo&quot;);
        logo.setAttribute(&quot;url&quot;,c.logo);
        card.addContent(logo);
      }
      cards.addContent(card);
    }
  }
  return new Document(cards);
}
</pre>
</td>
</tr>
</tbody>
</table>


A little logic and some GUI then completes the editor:

<img src="http://cs.au.dk/~amoeller/XML/programming/bcedit.gif" alt="GUI">

Compile with:&nbsp;<tt style="font-family:'Courier New',Courier,monospace; font-weight:bold">javac -classpath xerces.jar:jdom.jar BCedit.java</tt>

This example contains some general observations:



- XML documents are parsed via JDOM into&nbsp;**domain-specific data structures**- if the input is known to&nbsp;**validate**&nbsp;according to some schema, then many runtime errors can be assumed never to occur<li>how do we ensure that the output of&nbsp;<tt style="font-family:'Courier New',Courier,monospace; font-weight:bold">vector2doc</tt>&nbsp;is valid according to the schema? (well-formedness is for free)&nbsp;<br>
- that's a current research challenge!</li><li>
<pre name="code" class="java">import java.awt.*;
import java.awt.event.*;
import java.io.*; 
import java.util.*;
import org.jdom.*; 
import org.jdom.input.*; 
import org.jdom.output.*; 

class Card {
  public String name, title, email, phone, logo;

  public Card(String name, String title, String email, String phone, String logo) {
    this.name = name;
    this.title = title;
    this.email = email;
    this.phone = phone;
    this.logo = logo;
  }
}

public class BCedit extends Frame implements ActionListener {
  Button ok = new Button(&quot;ok&quot;);
  Button delete = new Button(&quot;delete&quot;);
  Button clear = new Button(&quot;clear&quot;);
  Button save = new Button(&quot;save&quot;);
  Button quit = new Button(&quot;quit&quot;);
  TextField name = new TextField(20);
  TextField title = new TextField(20);
  TextField email = new TextField(20);
  TextField phone = new TextField(20);
  TextField logo = new TextField(20);
  Panel cardpanel = new Panel(new GridLayout(0,1));
  String cardfile;
  Vector cardvector;
  int current = -1;

  public static void main(String[] args) { new BCedit(args[0]); }

  Vector doc2vector(Document d) {
    Vector v = new Vector();
    Iterator i = d.getRootElement().getChildren().iterator();
    while (i.hasNext()) {
      Element e = (Element)i.next();
      String phone = e.getChildText(&quot;phone&quot;);
      if (phone==null) phone=&quot;&quot;;
      Element logo = e.getChild(&quot;logo&quot;);
      String url;
      if (logo==null) url=&quot;&quot;; else url=logo.getAttributeValue(&quot;url&quot;);
      Card c = new Card(e.getChildText(&quot;name&quot;),
                        e.getChildText(&quot;title&quot;),
                        e.getChildText(&quot;email&quot;),
                        phone,
                        url);
      v.add(c);
    }
    return v;
  }

  Document vector2doc() {
    Element cards = new Element(&quot;cards&quot;);
    for (int i=0; i&lt;cardvector.size(); i&#43;&#43;) {
      Card c = (Card)cardvector.elementAt(i);
      if (c!=null) {
        Element card = new Element(&quot;card&quot;);
        Element name = new Element(&quot;name&quot;);
        name.addContent(c.name);
        card.addContent(name);
        Element title = new Element(&quot;title&quot;);
        title.addContent(c.title);
        card.addContent(title);
        Element email = new Element(&quot;email&quot;);
        email.addContent(c.email);
        card.addContent(email);
        if (!c.phone.equals(&quot;&quot;)) {
          Element phone = new Element(&quot;phone&quot;);
          phone.addContent(c.phone);
          card.addContent(phone);
        }
        if (!c.logo.equals(&quot;&quot;)) {
          Element logo = new Element(&quot;logo&quot;);
          logo.setAttribute(&quot;url&quot;,c.logo);
          card.addContent(logo);
        }
        cards.addContent(card);
      }
    }
    return new Document(cards);
  }

  void addCards() {
    cardpanel.removeAll();
    for (int i=0; i&lt;cardvector.size(); i&#43;&#43;) {
      Card c = (Card)cardvector.elementAt(i);
      if (c!=null) {
        Button b = new Button(c.name);
        b.setActionCommand(String.valueOf(i));
        b.addActionListener(this);
        cardpanel.add(b);
      }
    }
    this.pack();
  }

  public BCedit(String cardfile) {
    super(&quot;BCedit&quot;);
    this.cardfile=cardfile;
    try {
      cardvector = doc2vector(new SAXBuilder().build(new File(cardfile)));
    } catch (Exception e) {e.printStackTrace();}
    this.setLayout(new BorderLayout());
    ScrollPane s = new ScrollPane();
    s.setSize(200,0);
    s.add(cardpanel);
    this.add(s,BorderLayout.WEST);
    Panel l = new Panel(new GridLayout(5,1));
    l.add(new Label(&quot;Name&quot;));                  
    l.add(new Label(&quot;Title&quot;));                  
    l.add(new Label(&quot;Email&quot;));                  
    l.add(new Label(&quot;Phone&quot;));                  
    l.add(new Label(&quot;Logo&quot;));                  
    this.add(l,BorderLayout.CENTER);
    Panel f = new Panel(new GridLayout(5,1));
    f.add(name);    
    f.add(title);    
    f.add(email);    
    f.add(phone);    
    f.add(logo);    
    this.add(f,BorderLayout.EAST);
    Panel p = new Panel();
    ok.addActionListener(this);
    p.add(ok);
    delete.addActionListener(this);
    p.add(delete);
    clear.addActionListener(this);
    p.add(clear);
    save.addActionListener(this);
    p.add(save);
    quit.addActionListener(this);
    p.add(quit);
    this.add(p,BorderLayout.SOUTH);
    addCards();
    this.show();
  }

  public void actionPerformed(ActionEvent event) {
     Card c;
     String command = event.getActionCommand();
     if (command.equals(&quot;ok&quot;)) {
       c = new Card(name.getText(),
                    title.getText(),
                    email.getText(),
                    phone.getText(),
                    logo.getText());
       if (current==-1) {
          cardvector.add(c);
       } else {
          cardvector.setElementAt(c,current);
       }
       addCards();
     } else if (command.equals(&quot;delete&quot;)) {
        if (current!=-1) {
          cardvector.setElementAt(null,current);
          addCards();
        }
     } else if (command.equals(&quot;clear&quot;)) {
        current = -1;
        name.setText(&quot;&quot;);
        title.setText(&quot;&quot;);
        email.setText(&quot;&quot;);
        phone.setText(&quot;&quot;);
        logo.setText(&quot;&quot;);
     } else if (command.equals(&quot;save&quot;)) {
        try {
          new XMLOutputter().output(vector2doc(),new FileOutputStream(cardfile));
        } catch (Exception e) {e.printStackTrace();}
     } else if (command.equals(&quot;quit&quot;)) {
        System.exit(0);
     } else {
        current = Integer.parseInt(command);
        c = (Card)cardvector.elementAt(current);
        name.setText(c.name);
        title.setText(c.title);
        email.setText(c.email);
        phone.setText(c.phone);
        logo.setText(c.logo);
     }
  }
}</pre>
<br>
<br>
</li>